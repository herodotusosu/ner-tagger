import itertools

#
# Houses various different statistical tests and utility functions.
#

CHI_SQUARED_DF_1 = {
    0.995: 0.0000393,
    0.975: 0.000982,
    0.95: 0.004,
    0.90: 0.016,
    0.1: 2.706,
    0.05: 3.841,
    0.025: 5.024,
    0.01: 6.635,
    0.005: 7.879
}

def mcnemars(test1, test2, p):
    """
    Provide a McNemars statistical analysis on the given vectors of results. The
    vectors must align with subjects so that the first result from each test
    refers to the same item.

    Args:
    test1: A vector of results for the first test, where 0 means negative result
           and non-zero is positive result.
    test2: A vector of results for the second test, with the same element
           semantics, and to compare against test1.
    p: The level of significance, to check our final chi-squared value against
       to reject or support the null hypothesis. This p must be one of the
       following values, because for now I am pressed for time and cannot
       do the math to do arbitrary p-values: 0.995, 0.975, 0.95, 0.9, 0.1, 0.05,
       0.025, 0.01, 0.005.

    Returns:
    The results of the test with respect to the null hypothesis. If we reject
    the null, then False is returned, and if we accept the null True is returned
    """
    b = 0 # test1 positive, and test2 negative
    c = 0 # test1 negative, and test2 positive

    for sample1, sample2 in itertools.izip(test1, test2):
        if sample1 and not sample2:
            b += 1
        elif not sample1 and sample2:
            c += 1

    chi = ((b - c) * (b - c)) / (b + c)
    threshold = CHI_SQUARED_DF_1[p]

    return chi < threshold
