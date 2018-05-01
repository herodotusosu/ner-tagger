class AnalysisMatcher(object):
    """
    TODO:
    """

    def __init__(self, pos_feature_splitter=None, morph_feature_splitter=None):
        self.pos_feature_splitter = pos_feature_splitter
        self.morph_feature_splitter = morph_feature_splitter

        # The mapping from the pos coarse-grained tags, to the morphological
        # analyzers fine grained tags.
        self.rules = {}
        self.negs = {}
        self.white_list = set()


    def add_rule(self, pos_frag, *morph_frags):
        self.rules[pos_frag] = set(morph_frags)


    def add_white_list(self, pos_frag):
        """
        Add an item to the white list. If an analysis from the pos component is
        in the white list then it will automatically match. This is helpful if
        there is nothing to correlate between the analyses, and this is is an
        item you want to keep.

        Args:
        pos_frag: The pos fragment in the analysis we are matching on.
        """
        self.white_list.add(pos_frag)


    def add_neg(self, pos_frag, *neg_matches):
        self.negs[pos_frag] = set(neg_matches)


    def match(self, pos_analysis, morph_analysis):
        # Parse the POS and the morphological analyses. Add the entire pos just
        # in case, it is added as a rule.
        pos_components = self._parse_pos_analysis(pos_analysis)
        morph_components = self._parse_morph_analysis(morph_analysis)

        # For each component in the POS analysis, if a mapping rule exists for
        # it then check if there is any intersection between the map components
        # and the actual analysis.
        for pos_component in pos_components:
            if pos_component in self.white_list:
                return True

            try:
                mapped_morph_frags = self.rules[pos_component]
            except KeyError:
                continue

            try:
                neg_mapped_morph_frags = self.negs[pos_component]
            except KeyError:
                neg_mapped_morph_frags = set([])

            morphemes_hash = set(morph_components)

            # This morpheme analysis had a match with the expected morphological
            # analysis based on the POS tag.
            matches = morphemes_hash & mapped_morph_frags
            neg_matches = morphemes_hash & neg_mapped_morph_frags
            if matches and not neg_matches:
                return True

        return False


    def _parse_pos_analysis(self, analysis):
        if self.pos_feature_splitter:
            return analysis.split(self.pos_feature_splitter)

        return set([analysis])


    def _parse_morph_analysis(self, analysis):
        if self.morph_feature_splitter:
            return set(analysis.split(self.morph_feature_splitter))

        return set([analysis])
