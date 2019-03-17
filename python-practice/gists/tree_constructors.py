import abc

# Third party imports
import pandas as pd
    
# Internal module imports
from general_helpers import print_
from spgmi_utils_subset import sql
    

@abc.ABC  # This makes explicit that this class shouldn't be instantiated directly.
class TreeConstructor:
    def __init__(self, entity_col, tree_data, company_mapping):
        self.entity_col = entity_col
        self.tree_data = tree_data
        self.company_mapping = company_mapping
        self.l4_df = self.get_level_df(level=4)
        self.l3_df = self.get_level_df(level=3)
        self.l2_df = self.get_level_df(level=2)
        self.l1_df = self.get_level_df(level=1)
        self.missing_df = self.get_missing_bottom_level_df()
        self.l4_plus_other_df = pd.DataFrame(
            self.tree_data[pd.notnull(self.tree_data['L4'])][self.entity_col].values,
            columns=[self.entity_col]
        )
        self.l4_mappings_plus_other = self.tree_data.merge(self.l4_plus_other_df, how='inner', on=self.entity_col)
        self.l4_mappings = self.tree_data.merge(self.l4_df, how='inner', on=self.entity_col)
        self.l3_mappings = self.tree_data.merge(self.l3_df, how='inner', on=self.entity_col)
        self.l2_mappings = self.tree_data.merge(self.l2_df, how='inner', on=self.entity_col)
    
    def get_missing_bottom_level_df(self):
        other_df = pd.DataFrame(self.tree_data[pd.notnull(self.tree_data['L4'])]
                                [self.entity_col].values, columns=[self.entity_col])
        return pd.concat([other_df, self.l4_df, self.l4_df]).drop_duplicates(keep=False)
    
    def get_level_df(self, level):
        if level == 1:
            return pd.DataFrame(self.tree_data[pd.isnull(self.tree_data['L2'])]
                                [self.entity_col].values, columns=[self.entity_col])
        if level == 2:
            return pd.DataFrame(self.tree_data[pd.isnull(self.tree_data['L3'])].
                                merge(self.tree_data[pd.notnull(self.tree_data['L2'])][[self.entity_col]],
                                        how='inner',
                                        on=self.entity_col)
                                [self.entity_col].values, columns=[self.entity_col])
        if level == 3:
            return pd.DataFrame(self.tree_data[pd.isnull(self.tree_data['L4'])].
                                merge(self.tree_data[pd.notnull(self.tree_data['L3'])][[self.entity_col]],
                                        how='inner',
                                        on=self.entity_col)
                                [self.entity_col].values, columns=[self.entity_col])
        if level == 4:
            return pd.DataFrame(self.tree_data[pd.notnull(self.tree_data['L4'])]
                                ['L4'].unique(), columns=[self.entity_col])
    

"""
You could if you want to leverage composition over inheritance here, maybe creating a data_getter? That way you only have one
object (tree data), but you specify how it gets its data. I would need to think through that a bit I think.  
"""
class IndustryData(TreeConstructor):
    def __init__(self):
        self.company_mapping = self._get_industry_company_mapping()
        self.tree_data = self._get_industry_tree_data()
        TreeConstructor.__init__(self, 'KeyMIIndustryTree', self.tree_data, self.company_mapping)
    
    def _get_industry_tree_data(self):
        print_(['Pulling back industry tree data from DMS'])
        query = """
            select
                    KeyMIIndustryTree,
                    KeyIndustryTreeLevel1 as L1,
                    KeyIndustryTreeLevel2 as L2,
                    KeyIndustryTreeLevel3 as L3,
                    KeyIndustryTreeLevel4 as L4
                from Lookup..MIIndustryTree
                where updOperation <> 2
                and KeyMIIndustryTree not in (4000, 4001, 4002)
            """
        data = sql.query_sql(query, server='SNLSQLDEV')
        return data
    
    def _get_industry_company_mapping(self):
        print_(['Pulling back industry tree to company mapping from DMS'])
        query = """
            select
                KeyInstn,
                KeyMIIndustryTree
            from Calcs..InstnMIIndustry
            where updOperation <> 2
            """
        data = sql.query_sql(query, server='SNLSQLDEV')
        return data
    
    
class GeographyData(TreeConstructor):
    def __init__(self):
        entity_col = 'KeyGeographyTree'
        tree_raw_data = self._get_geo_tree_data()
        tree_data = self._get_leveled_values()
        company_mapping = self._get_geography_company_mapping()
        TreeConstructor.__init__(self,  self.entity_col, self.tree_data, self.company_mapping)
    
    def _get_geography_company_mapping(self):
        print_(['Pulling back geography tree to company mapping from DMS'])
        query = """
            select
                i.KeyInstn,
                i.KeyGeographyTree
            from SNL..Instn i
            where i.updOperation <> 2
            and i.InstnCurrent = 1
            """
        data = sql.query_sql(query)
        return data
    
    def _get_geo_tree_data(self):
        print_(['Pulling back geography tree data from DMS'])
        query = """
            select
                KeyGeographyTree,
                KeyGeographyTreeParent
            from Lookup..GeographyTree
            where updOperation <> 2
            """
        data = sql.query_sql(query)
        return data
    
    def _get_leveled_values(self):
        geo_df_list = []
        for level in ['L1', 'L2', 'L3', 'L4', 'L5', 'L6', 'L7']:
            print_([level])
            if level == 'L1':
                geo_df = self.tree_raw_data[self.tree_raw_data.KeyGeographyTreeParent.map(lambda x: str(x) == 'nan')][
                    [self.entity_col]]
                geo_df = geo_df.rename(columns={self.entity_col: level})
                geo_df_list.append(geo_df)
            else:
                geo_df = geo_df_list[-1].merge(self.tree_raw_data[[self.entity_col, 'KeyGeographyTreeParent']],
                                                how='left',
                                                left_on='L' + str(int(level.replace('L', '')) - 1),
                                                right_on='KeyGeographyTreeParent')
                geo_df = geo_df.drop(['KeyGeographyTreeParent'], axis=1)
                geo_df = geo_df.rename(columns={self.entity_col: level})
                geo_df = geo_df[geo_df[level].map(lambda x: str(x) != 'nan')]
                geo_df_list.append(geo_df)
        all_levels = pd.concat(geo_df_list)
        all_levels[self.entity_col] = all_levels['L7'].fillna(all_levels['L6']).fillna(all_levels['L5']).fillna(
            all_levels['L4']).fillna(all_levels['L3']).fillna(all_levels['L2']).fillna(all_levels['L1'])
        return all_levels
    
    
def add_child_counts(level_df: pd.DataFrame,
                        child_df: pd.DataFrame = None,
                        mapping_df: pd.DataFrame = None,
                        mapping_col: str = None,
                        user_id: str = None,
                        entity_id: str = None) -> pd.DataFrame:
    """ From a dataframe of user to entity to click counts, a child dataframe of user to entity to click counts,
        and a mapping dataframe of entity to children entities, return the count of clicks from child entities
    
        Parameters
        ----------
    
        level_df: df
        df of desired entity clicks
    
        child_df: df
        df of entity to click counts for children entities of level dataframe
    
        mapping_df:
        df providing map between level data frame entities and child df entities
    
        mapping_col: string
        name of mapping col
    
        user_id: string
        name of user_id column
    
        entity_id: string
        name of entity column
        Returns
        -------
        df: df
        df with new column 'children_value' representing the clicks to an entity from the children entities
    
    
        """
    # filter the test_logs down to only user and EntityTypes we've seen before
    # we should probably default to a generic prediction instead of eliminating new users
    # probably need to abstract this out a bit more
    print_(['Add column \'child counts\' to level df'])
    if child_df is not None:
        child_df = child_df.copy()
        child_df['real_plus_children_value'] = child_df['real_value'] + child_df['children_value']
        child_df = child_df.merge(mapping_df[[entity_id, mapping_col]], how='left',
                                    on=entity_id)  # mapping the child Key to the desired parent Key
        child_df = child_df[[user_id, mapping_col, 'real_plus_children_value']].groupby(
            [user_id, mapping_col]).sum()  # get counts of KOU and desired parent Key
        child_df.columns = ['children_value']
        df = level_df.merge(child_df, how='outer', left_on=[user_id, entity_id],
                            right_on=[user_id, mapping_col])  # add the child_value col to the level df
        df['children_value'] = df['children_value'].fillna(0)
    
    else:
        df = level_df.copy()
        df['children_value'] = 0
    return df
    
    
def add_parent_counts(level_df: pd.DataFrame,
                        parent_df: pd.DataFrame = None,
                        mapping_df: pd.DataFrame = None,
                        parent_mapping_col: str = None,
                        user_id: str = None,
                        entity_id: str = None) -> pd.DataFrame:
    """ From a dataframe of entity to click counts, a parent data frame of entity to click counts,
        and a mapping data frame of entity to parent entities, return the count of clicks from parent entities
        equally divided between all children
    
        Parameters
        ----------
    
        level_df: df
        df of desired entity clicks
    
        parent_df: df
        df of entity to click counts for parent entities of level dataframe
    
        mapping_df:
        df providing map between level data frame entities and parent df entities
    
        parent_mapping_col: string
        name of mapping col
    
        user_id: string
        name of user_id column
    
        entity_id: string
        name of entity column
        Returns
        -------
        df: df
        df with new column 'parent_value' representing the clicks to an entity from the parent entitiy
    
        """
    if parent_df is not None:
        parent_df = parent_df.copy()
        parent_df['real_plus_parent_value'] = parent_df['real_value'] + parent_df['parent_value']
        count_df = mapping_df[parent_mapping_col].value_counts()
        count_df = count_df.reset_index()
        count_df.columns = [parent_mapping_col, 'num_children']
        parent_df.rename(columns={entity_id: parent_mapping_col}, inplace=True)
        parent_df = parent_df.merge(mapping_df, how='inner', on=parent_mapping_col)  # Not all "parents" have children
        parent_df = parent_df.merge(count_df, how='left', on=parent_mapping_col)
        parent_df['parent_value'] = parent_df['real_plus_parent_value'] / parent_df['num_children']  # evenly split the
        # parent click counts among all children found from DMS pull
        df = level_df.merge(parent_df[[user_id, 'parent_value', entity_id]], how='outer', on=[user_id, entity_id])
        df['parent_value'] = df['parent_value'].fillna(0)
    else:  # this else block should be running in case passing top level of the tree count dataframe
        df = level_df.copy()
        df['parent_value'] = 0
    return df
    
    
def get_counts(df: pd.DataFrame,
                user_id: str,
                entity_col: str,
                count_col: str) -> pd.DataFrame:
    """ From a dataframe of user, entity, and clicks, return click counts for each user/entity pair
    
    Parameters
    ----------
    
    df: df
        df of clicks
    
    user_id: string
        name of user_id column
    
    entity_col: string
        name of entity column
    
    count_col: string
        name of columns with click counts
    Returns
    -------
    loss: df
        df from user/entity pair to click counts
    
        """
    return df[[user_id, entity_col, count_col]].groupby([user_id, entity_col]).sum()
    
    
def add_missing_pairs(df: pd.DataFrame,
                        users_df: pd.DataFrame,
                        entities_df: pd.DataFrame,
                        user_id: str,
                        entity_id: str,
                        count_col: str) -> pd.DataFrame:
    """ Identifies missing observed user/entity pairs and sets their count_col to be zeros
        This allows us to track and return probabilities for all user/entity pairs
        Even when there is no observed click pairing between the two
    
        Parameters
        ----------
    
        df: df
        df of user to entity pairs and click counts
    
        users_df: df
        df of all users you want predictions for
    
        entities_df: df
        df of all entities you want predictions for
    
        user_id: string
        name of user_id column
    
        entity_id: string
        name of entity column
    
        count_col: string
        name of columns with click counts
    
        Returns
        -------
        loss: df
        df with additional missing user/entity pairs from the original df
    
        """
    print_(['Adding missing pairs to dataframe'])
    
    def create_all_pairs_map(df1, df2):
        df1 = df1.copy()
        df2 = df2.copy()
        df1['join'] = 1
        df2['join'] = 1
        df_both = df1.merge(df2, how='outer', on='join')  # df of all possible user/entity pairs
        return df_both.drop(columns=['join'])
    
    def get_missing_pairs(tree, pairs):
        df_pairs = pairs.merge(tree, how='outer', on=[user_id, entity_id])  # add possible but not yet observed
        # user/entity pairs
        df_pairs[count_col] = df_pairs[count_col].fillna(0)
        df_pairs.reset_index(inplace=True)
        return df_pairs
    
    pairs_df = create_all_pairs_map(users_df, entities_df)
    return get_missing_pairs(tree=df, pairs=pairs_df)
    
    
def get_tree(tree_obj: TreeConstructor,
                log_file: pd.DataFrame,
                unit_df: pd.DataFrame,
                unit_id: str,
                count_col_id: str) -> pd.DataFrame:
    """ From a tree object, a log file of clicks, and a dataframe of users,
        return df with user/entity pairs to 'parent_value' counts, 'children_value' counts, and 'real_value' counts
        'real value' indicates an actual click on that entity, not a pseudo click coming from a parent or child
    
        Parameters
        ----------
    
        tree_obj: TreeConstructor
        manipulation of raw DMS data into common format object
    
        log_file: df
        usage log file of user to entity pairs
    
        unit_df: df
        df of all users you want predictions for
    
        unit_id: string
        name of user_id column in log_file and unit_df dataframes
    
        count_col_id: string
        name of column with click counts
    
        Returns
        -------
        loss: df
        df with additional missing user/entity pairs from the original df
    
        """
    l1_logs = log_file.merge(tree_obj.l1_df, how='inner', on=tree_obj.entity_col)  # filtering to top level click logs
    l2_logs = log_file.merge(tree_obj.l2_df, how='inner', on=tree_obj.entity_col)  # filtering to 2nd level click logs
    l3_logs = log_file.merge(tree_obj.l3_df, how='inner', on=tree_obj.entity_col)  # filtering to 3rd level click logs
    l4_logs = log_file.merge(tree_obj.l4_df, how='inner', on=tree_obj.entity_col)  # filtering to 4th level click logs
    other_logs = log_file.merge(tree_obj.missing_df, how='inner', on=tree_obj.entity_col)
    
    l4_tree_df = (l4_logs.
                    pipe(get_counts, user_id=unit_id, entity_col=tree_obj.entity_col, count_col=count_col_id).
                    pipe(add_missing_pairs, users_df=unit_df, entities_df=tree_obj.l4_df, user_id=unit_id,
                        entity_id=tree_obj.entity_col, count_col=count_col_id))
    
    l3_tree_df = (l3_logs.
                    pipe(get_counts, user_id=unit_id, entity_col=tree_obj.entity_col, count_col=count_col_id).
                    pipe(add_missing_pairs, users_df=unit_df, entities_df=tree_obj.l3_df, user_id=unit_id,
                        entity_id=tree_obj.entity_col, count_col=count_col_id))
    
    l2_tree_df = (l2_logs.
                    pipe(get_counts, user_id=unit_id, entity_col=tree_obj.entity_col, count_col=count_col_id).
                    pipe(add_missing_pairs, users_df=unit_df, entities_df=tree_obj.l2_df, user_id=unit_id,
                        entity_id=tree_obj.entity_col, count_col=count_col_id))
    
    l1_tree_df = (l1_logs.
                    pipe(get_counts, user_id=unit_id, entity_col=tree_obj.entity_col, count_col=count_col_id).
                    pipe(add_missing_pairs, users_df=unit_df, entities_df=tree_obj.l1_df, user_id=unit_id,
                        entity_id=tree_obj.entity_col, count_col=count_col_id))
    
    other_counts_df = get_counts(other_logs, user_id=unit_id, entity_col=tree_obj.entity_col, count_col=count_col_id)
    other_tree_df = other_counts_df.reset_index(inplace=False)
    
    other_tree_child_df = add_child_counts(level_df=other_tree_df)
    l4_tree_child_df = add_child_counts(level_df=l4_tree_df,
                                        child_df=other_tree_child_df,
                                        mapping_df=tree_obj.l4_mappings_plus_other[[tree_obj.entity_col, 'L4']],
                                        mapping_col='L4',
                                        user_id=unit_id,
                                        entity_id=tree_obj.entity_col)
    l3_tree_child_df = add_child_counts(level_df=l3_tree_df,
                                        child_df=l4_tree_child_df,
                                        mapping_df=tree_obj.l4_mappings_plus_other[[tree_obj.entity_col, 'L3']],
                                        mapping_col='L3',
                                        user_id=unit_id,
                                        entity_id=tree_obj.entity_col)
    l2_tree_child_df = add_child_counts(level_df=l2_tree_df,
                                        child_df=l3_tree_child_df,
                                        mapping_df=tree_obj.l3_mappings[[tree_obj.entity_col, 'L2']],
                                        mapping_col='L2',
                                        user_id=unit_id,
                                        entity_id=tree_obj.entity_col)
    l1_tree_child_df = add_child_counts(level_df=l1_tree_df,
                                        child_df=l2_tree_child_df,
                                        mapping_df=tree_obj.l2_mappings[[tree_obj.entity_col, 'L1']],
                                        mapping_col='L1',
                                        user_id=unit_id,
                                        entity_id=tree_obj.entity_col)
    
    l1_tree_child_parent_df = add_parent_counts(level_df=l1_tree_child_df)
    l2_tree_child_parent_df = add_parent_counts(level_df=l2_tree_child_df,
                                                parent_df=l1_tree_child_parent_df,
                                                mapping_df=tree_obj.l2_mappings[[tree_obj.entity_col, 'L1']],
                                                parent_mapping_col='L1',
                                                user_id=unit_id,
                                                entity_id=tree_obj.entity_col)
    l3_tree_child_parent_df = add_parent_counts(level_df=l3_tree_child_df,
                                                parent_df=l2_tree_child_parent_df,
                                                mapping_df=tree_obj.l3_mappings[[tree_obj.entity_col, 'L2']],
                                                parent_mapping_col='L2',
                                                user_id=unit_id,
                                                entity_id=tree_obj.entity_col)
    l4_tree_child_parent_df = add_parent_counts(level_df=l4_tree_child_df,
                                                parent_df=l3_tree_child_parent_df,
                                                mapping_df=tree_obj.l4_mappings[[tree_obj.entity_col, 'L3']],
                                                parent_mapping_col='L3',
                                                user_id=unit_id,
                                                entity_id=tree_obj.entity_col)
    
    l1_tree_child_parent_df['level'] = 1
    l2_tree_child_parent_df['level'] = 2
    l3_tree_child_parent_df['level'] = 3
    l4_tree_child_parent_df['level'] = 4
    
    counts = log_file[[unit_id, count_col_id]].groupby(unit_id).sum()
    counts.columns = ['num_hits']
    all_data = l4_tree_child_parent_df.append(l3_tree_child_parent_df).append(l2_tree_child_parent_df).append(
        l1_tree_child_parent_df)
    all_data = all_data.merge(counts, how='left', left_on=unit_id, right_index=True)
    all_data['num_hits'] = all_data['num_hits'].fillna(0)
    return all_data
    
    
def get_tree_flat(log_file: pd.DataFrame,
                    unit_df: pd.DataFrame,
                    cs_df: pd.DataFrame,
                    unit_id: str,
                    count_col_id: str,
                    entity_col: str) -> pd.DataFrame:
    """ From just a log file of clicks, a data frame of users, and a dataframe of possible content sets
        return df 'real_value' counts. This function assumes no tree structure to click data
        no parent or child structure since content set values have no hierarchical structure to them
    
    Parameters
        ----------
    
    log_file: df
        usage log file of user to entity pairs
    
    unit_df: df
        df of all users you want predictions for
    
    cs_df: df
            df of all content sets you want predictions for
    
    unit_id: string
        name of user_id column
    
    count_col_id: string
        name of columns with click counts
    
    entity_col: string
        name of entity column
    
    Returns
    -------
    loss: df
        df with additional missing user/entity pairs from the original df
    
        """
    df = get_counts(log_file, user_id=unit_id, entity_col=entity_col, count_col=count_col_id)
    df = add_missing_pairs(df,
                            users_df=unit_df,
                            entities_df=cs_df,
                            user_id=unit_id,
                            entity_id=entity_col, count_col=count_col_id)
    user_counts = log_file[[unit_id, count_col_id]].groupby(unit_id).sum()
    user_counts.columns = ['num_hits']
    all_data = df.merge(user_counts, how='left', left_on=unit_id, right_index=True)
    all_data['num_hits'] = all_data['num_hits'].fillna(0)
    return all_data
