from psycopg2.extensions import AsIs



class PhonFeats:
    """
    This class provides utility functions to work with segments in the IPA.
    Takes two lists of strings (segments and a language inventory (optional, 
    only if you intend to use contrastive_features()))
    """

    UNIVALENT = ['labial', 'coronal', 'dorsal']

    def __init__ (self, curs, segments, inventory=None):
        """
        Class constructor; sets up a temporary table to work with.
        The temp table contains only the segments specified in the inventory, 
        otherwise if none are passed in, defaults to all segments
        """

        self.cur = curs
        self.seg = segments  # segment list
        self.inv = inventory  # inventory list for a language

        d = 'DROP TABLE IF EXISTS tmp'
        self.cur.execute(d)
        # symbol, cons, son, approx, continuant, nasal, lat, voice, spread_gl, labial, coronal, dist, anterior, strident, dorsal, high, back

        if inventory != None:
            q ="""
            CREATE TEMP TABLE tmp AS
            SELECT *
            FROM features
            WHERE symbol IN %s"""
            self.cur.execute(q, (inventory,))
        else:
            q ="""
            CREATE TEMP TABLE tmp AS
            SELECT *
            FROM features"""
            self.cur.execute(q)


    @classmethod
    def list_to_dict(cls, featlist:list) -> dict:

        d = {}
        for item in featlist: 
            d[item[1:]] = item[0]
        return d

    @classmethod
    def dict_to_list(cls, d:dict) -> list:

        l = []
        for key in d: l.append(d[key]+key)
        return l

    def get_feat_labels(self) -> list:
        """
        returns feature labels from the feature table
        """

        self.cur.execute("SELECT * FROM tmp LIMIT 0")
        colnames = [desc[0] for desc in self.cur.description] 
        return colnames[1:]

    
    def segment_feature_list(self, segment):
        """
        returns the feature specification for a single segment given as a string
        """

        features_list = []
        colnames = self.get_feat_labels()

        q = 'SELECT * FROM tmp WHERE symbol LIKE %s'
        self.cur.execute(q, (segment,))
        x = self.cur.fetchone()

        y = 1
        for i in colnames:
            features_list.append(x[y]+i)
            y = y+1
            
        return features_list



    def seg_feat_match(self, features):
        """
        Finds all segments in the inventory that match the feature specification given, and returns the segment list as a list of strings.

        @param features (list of strings); example: ['+cons', '-voice', '+dorsal']
        """

        dict_feats = self.list_to_dict(features)
        pos_feat, neg_feat = (() for i in range(2))
        segments = []

        for key in dict_feats:
            if dict_feats[key] == "+": pos_feat+=(key,)
            else: neg_feat+=(key,)

        query = """
        SELECT *
        FROM tmp
        WHERE TRUE """
        
        condpos ="""
        AND '+' IN %(pos)s AND '-' NOT IN %(pos)s AND '0' NOT IN %(pos)s"""
        condneg= """
        AND '-' IN %(neg)s AND '+' NOT IN %(neg)s AND '0' NOT IN %(neg)s"""

        if len(pos_feat)!= 0: query += condpos
        if len(neg_feat)!= 0: query += condneg

        pos = tuple(map(AsIs,pos_feat))
        neg = tuple(map(AsIs,neg_feat))

        self.cur.execute(query, {'pos':pos, 'neg':neg})
        x = self.cur.fetchall()

        for i in range(0,len(x)): segments.append(x[i][0])
        return segments

        
    # TODO: have this return a dictionary instead
    # TODO: instead of passing in a boolean, have the function take a list of segments instead
    def features_common(self,inv_check):
        """
        Finds all features in common with the class' segments, and returns it 
        as a list.

        @param inv_check (bool): whether or not to check the inventory or the 
        list of segments given in the class
        """

        if inv_check:
            tmp = self.inv
        else:
            tmp = self.seg

        q = 'SELECT COUNT(*) FROM tmp WHERE symbol IN %s'
        self.cur.execute(q, (tmp,))
        x = self.cur.fetchone()

        n = x[0]
        features_list = []
        features_labels = self.get_feat_labels()

        
        #TODO: rewrite this so it doesn't use a for-loop
        for i in features_labels:
            q = """
            WITH temp AS(
                SELECT * FROM features WHERE symbol IN %s
                ) 
            SELECT 
            """ +i +" ,count(symbol) FROM temp GROUP BY "+i+ " ORDER BY "+ i


            self.cur.execute(q, (tmp,))
            x = self.cur.fetchall()

            if x[0][1] == n:
                if  x[0][0]=="+": features_list.append("+"+i) 
                elif x[0][0]=="-": features_list.append("-"+i) 
                elif x[0][0]== "0": features_list.append("0"+i)

        return features_list


    def features_uncommon(self, inv_check):
        """
        returns all features uncommon to the segments/inventory
        """

        if inv_check:
            t = self.inv
        else:
            t = self.seg

        q = 'SELECT COUNT(*) FROM tmp WHERE symbol IN %s'
        self.cur.execute(q, (t,))
        x = self.cur.fetchone()

        n = x[0]
        features_labels = self.get_feat_labels()

        common = self.features_common(inv_check)
        common_new = []

        #remove feature value from common list:
        for i in common:
            common_new.append(i[1:])

        #now, find difference
        s = set(common_new)
        retval = [x for x in features_labels if x not in s]

        return retval

    #variables for computing minimal and contrastive features
    lensmallest = None
    currentminimal = None
    listoftried = []


    def check_match(self, featlist) -> bool:
        """
        Helper function for finding minimal features; checks if a feature specification
        list matches the class' segments
        """

        #grab the segments that match the feature specification given in featlist
        match = self.seg_feat_match(featlist)

        #if those features give back all the segments in the segments list, then return true
        if set(match) == set(self.seg): return True
        else: return False
    

    def min_feats(self):
        """
        Finds minimal feature specification for the class' segments.
        """

        #initialize variables before recursion
        root = self.features_common(False) #root
        PhonFeats.currentminimal = root  #current smallest specification
        PhonFeats.lensmallest = len(root)  #length of the current smallest 
        #specification
        
        #TODO: abstract this out
        # returns only the feature names of a common feature list
        def remover(u):
            retval = []
            for item in u: retval.append(item[1:])
            return retval

        toremove = remover(root)

        for item in toremove:
            # attempt to discard a feature value and see if it holds
            self.recurse(root,item, True)

        retval = PhonFeats.currentminimal
        PhonFeats.lensmallest = None
        PhonFeats.currentminimal = None
        PhonFeats.listoftried = []

        return retval


    def recurse(self, featlist, to_remove, minimal):
        """
        Recursive helper function to find minimal and contrastive features.

        @param featlist (list of strings): list of features that should be tried to see if it is (currently) minimal/contrastive, after removing to_remove from it
        @param to_remove (string): item that should be removed from featlist before checking featlist
        @param (bool): whether or not we are checking for minimal features or contrastive features
        """

        # depending on the value of minimal, runs different check functions
        def check(x):
            n = len(x)
            if (n < PhonFeats.lensmallest):
                if minimal:
                    if (self.check_match(x)):
                        PhonFeats.currentminimal = x
                        PhonFeats.lensmallest = n
                else:
                    if (self.check_contrast(x)):
                        PhonFeats.currentminimal = x
                        PhonFeats.lensmallest = n

                

        #remove to_remove from featlist and check it, then store it in checked
        featlist_removed = [i for i in featlist if not (to_remove in i)]
        check(featlist_removed)
        PhonFeats.listoftried.append(set(featlist_removed))

        
        # base case:
        if len(featlist_removed) <= 1:
            return PhonFeats.currentminimal

        # recursive step:
        else:
            for item in featlist_removed:
                see_featlist_removed = [i for i in featlist_removed if not (item in i)]

                #only try if not tried before, and it is smaller than the current smallest
                if (set(see_featlist_removed) not in PhonFeats.listoftried) and (len(see_featlist_removed) < PhonFeats.lensmallest):
                    self.recurse(featlist_removed,item, minimal)



    d = {}
    def compute_inventory_dict(self):
        """
        computes a dictionary of features for the inventory of the class
        """

        for i in self.inv:
            feats = self.segment_feature_list(i)
            PhonFeats.d[i] = feats



    def check_contrast(self, featlist) -> bool:
        """
        given a list of tentative features, check if those features contrast all segments in the inventory
        """

        maslist = []

        # grab the feature specification for each segment in the language's inventory
        for i in self.inv:
            feats = PhonFeats.d[i]
            l = []
            #grabs only the features for i that are specified in featlist
            for y in featlist:
                result = [x for x in feats if y in x]  
                l.append(result[0])

            # print(l)
            maslist.append((l))

        checking = (len(set(map(tuple,maslist))) != len(maslist))

        return not checking



    def contrastive_features(self):
        """
        Returns the minimal amount of features needed to contrast segments in the inventory.
        Needs an inventory to be specified for the class
        """

        self.compute_inventory_dict()
        root = self.features_uncommon(True)
        PhonFeats.lensmallest = len(root)
        PhonFeats.currentminimal = root

        #start the recursion sequence
        for item in root:
            self.recurse(root, item, False)

        retval = PhonFeats.currentminimal
        PhonFeats.lensmallest = None
        PhonFeats.currentminimal = None
        PhonFeats.listoftried = []

        return retval


    # function to calculate feature economy score for a given language
    def get_economy_score(self):
        S = len(self.inv)
        F = len(self.contrastive_features())
        E = S/F
        return E


