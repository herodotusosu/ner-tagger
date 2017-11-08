import operator


class FeatureStore(object):
    """
    TODO
    """
    def __init__(self):
        self.store = {}
        self.order = {}
        self.singletons = set()


    def add_singleton(self, feature, order):
        self.singletons.add(feature)
        self.order[feature] = order
        self.store[feature] = set([feature])


    def add_key(self, key, order):
        self.order[key] = order
        self.store[key] = []


    def add_feature(self, key, feat):
        self.store[key].append(feat)


    def output(self, separator='\t'):
        line_items = []
        sorted_items = sorted(self.order.items(), key=operator.itemgetter(1))
        for key, _ in sorted_items:
            if key in self.singletons:
                line_items.append(key)
            else:
                features = self.store[key]

                for feature in features:
                    line_items.append(key + '=' + feature)

        final = separator.join(line_items)
        return final
