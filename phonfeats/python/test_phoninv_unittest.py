import pytest
import sys
# sys.path.insert(0, 'phonfeats\python')
import phon_inv  as piv
import init as ini

#TODO: change test discovery

def f():
    raise SystemExit(1)

class TestFeatLabels:

    # def test_one(self):
    #     x = piv.PhonFeats(ini.connect(),('p', 't', 'v'))
    #     assert x.get_feat_labels == ['cons', 'son', 'syll', 'labial', 'round', 'coronal', 'anterior', 'dist', 'dorsal', 'high', 'low', 'back', 'tense', 'voice', 'spread_gl', 'constr_gl', 'continuant', 'strident', 'lat', 'delayed_release', 'nasal', 'stress', 'long', 'approx', 'tap', 'trill', 'labiodental', 'front']

    def test_two(self):
        pass
        # def test_one(self):

class TestSegFeatList:
    hawaiian = ('m', 'n', 'p', 'k', 'ʔ', 'h', 'w', 'l')
    def test_one(self):
        x = piv.PhonFeats(ini.connect(),('p'), TestSegFeatList.hawaiian)
        correct = ['+cons', '+son', '-syll', '-labial', '-round', '+coronal', '+anterior', '-dist', '-dorsal', '0high', '0low', '0back', '0tense', '+voice', '-spread_gl', '-constr_gl', '-continuant', '-strident', '-lat', '0delayed_release', '+nasal', '-stress', '-long', '-approx', '-tap', '-trill', '-labiodental', '0front']
        test = x.segment_feature_list('n')
        assert set(correct) == set(test)


class TestFeatCommon:
    def test_one(self):
        x = piv.PhonFeats(ini.connect(),('p', 't', 'k', 'b', 'd', 'g', 'f', 's', 'ʃ', 'h', 'm', 'n', 'ŋ', 'r', 'l', 'j','ʋ'))
        correct = ['-syll', '-round', '-constr_gl', '-stress', '-long', '-tap']
        test = x.features_common(False)
        assert set(correct) == set(test)

class TestFeatUncommon:
    x = piv.PhonFeats(ini.connect(),('p', 't', 'v'))
    def test_one(self):
        correct = ['labial', 'coronal', 'anterior', 'dist', 'voice', 'continuant', 'strident', 'delayed_release', 'labiodental']
        
        test = TestFeatUncommon.x.features_uncommon(False)
        assert set(correct) == set(test)

    def test_two(self):
        nae = ('p', 't', 'k', 'ʔ', 'b', 'd', 'g', 'f', 'θ', 's', 'ʃ', 'h', 'v', 'ð', 'z', 'ʒ', 't͡ʃ', 'd͡ʒ', 'm', 'n', 'ŋ', 'l', 'ɹ', 'w', 'j', 'i', 'ɪ', 'u', 'ʊ', 'e', 'ɛ', 'ə', 'ʌ', 'ɔ', 'æ', 'ɑ')
        x = piv.PhonFeats(ini.connect(),('p', 't', 'k', 'b', 'd', 'g', 'f', 's', 'ʃ', 'h', 'm', 'n', 'ŋ', 'r', 'l', 'j','ʋ'))
        # print("LOOK: ", x.features_common())

        correct = ['cons', 'son', 'labial', 'coronal', 'anterior', 'dist', 'dorsal', 'high', 'low', 'back', 'tense', 'voice', 'spread_gl', 'continuant', 'strident', 'lat', 'delayed_release', 'nasal', 'approx', 'trill', 'labiodental', 'front']
        test = x.features_uncommon(False)
        assert set(correct) == set(test)

    def test_three(self):
        fin = ('p', 't', 'k', 'b', 'd', 'g', 'f', 's', 'ʃ', 'h', 'm', 'n', 'ŋ', 'r', 'l', 'j','ʋ' )
        x = piv.PhonFeats(ini.connect(), ('p', 't', 'k', 'g'),fin)
        correct = ['cons', 'son', 'labial', 'coronal', 'anterior', 'dist', 'dorsal', 'high', 'low', 'back', 'tense', 'voice', 'spread_gl', 'continuant', 'strident', 'lat', 'delayed_release', 'nasal', 'approx', 'trill', 'labiodental', 'front']
        test = x.features_uncommon(True)
        assert set(correct) == set(test)
        
    def test_four(self):
        fin = ('p', 't', 'k', 'b', 'd', 'g', 'f', 's', 'ʃ', 'h', 'm', 'n', 'ŋ', 'r', 'l', 'j','ʋ' )
        x = piv.PhonFeats(ini.connect(), ('p', 't', 'k', 'g'),fin)
        correct = ['labial', 'coronal', 'anterior', 'dist', 'dorsal', 'high', 'low', 'voice', 'strident']
        test = x.features_uncommon(False)
        assert set(correct) == set(test)

class TestCheckMatch:
    nae = ('p', 't', 'k', 'ʔ', 'b', 'd', 'g', 'f', 'θ', 's', 'ʃ', 'h', 'v', 'ð', 'z', 'ʒ', 't͡ʃ', 'd͡ʒ', 'm', 'n', 'ŋ', 'l', 'ɹ', 'w', 'j', 'i', 'ɪ', 'u', 'ʊ', 'e', 'ɛ', 'ə', 'ʌ', 'ɔ', 'æ', 'ɑ')

    def test_one(self):
        
        x = piv.PhonFeats(ini.connect(),('p', 't', 'k'),TestCheckMatch.nae)
        correct = True
        test = x.check_match(['+cons', '-son', '-syll', '-round', '-voice', '-spread_gl', '-constr_gl', '-continuant', '-lat', '-delayed_release', '-nasal', '-stress', '-long', '-approx', '-tap', '-trill', '-labiodental'])
        assert correct == test

    def test_two(self):
        
        x = piv.PhonFeats(ini.connect(),('i', 'ɪ', 'u', 'ʊ'),TestCheckMatch.nae)
        correct = True
        test = x.check_match(['+syll', '+high'])
        assert correct == test

    def test_three(self):

        x = piv.PhonFeats(ini.connect(),('v', 'z', 'ʒ', 'ð'),TestCheckMatch.nae)
        correct = True
        test = x.check_match(['-son', '+voice', '+continuant'])
        assert correct == test

    def test_four(self):

        x = piv.PhonFeats(ini.connect(),('v', 'z', 'ʒ', 'ð'),TestCheckMatch.nae)
        correct = True
        test = x.check_match(['+voice', '+continuant', '-approx'])
        assert correct == test

    def test_five(self):

        x = piv.PhonFeats(ini.connect(),('d', 'z', 'n', 'l'),TestCheckMatch.nae)
        correct = True
        test = x.check_match(['+voice', '-dist'])
        assert correct == test

class TestMinFeat:
    nae = ('p', 't', 'k', 'ʔ', 'b', 'd', 'g', 'f', 'θ', 's', 'ʃ', 'h', 'v', 'ð', 'z', 'ʒ', 't͡ʃ', 'd͡ʒ', 'm', 'n', 'ŋ', 'l', 'ɹ', 'w', 'j', 'i', 'ɪ', 'u', 'ʊ', 'e', 'ɛ', 'ə', 'ʌ', 'ɔ', 'æ', 'ɑ')

    def test_one(self):
        x = piv.PhonFeats(ini.connect(),('d', 'z', 'n', 'l'),TestMinFeat.nae)
        correct = ['+voice', '-dist']
        test = x.min_feats()
        assert set(correct) == set(test)

    def test_two(self):
        x = piv.PhonFeats(ini.connect(),('v', 'z', 'ʒ', 'ð'),TestMinFeat.nae)
        correct = ['+voice', '+continuant', '-approx']
        test = x.min_feats()
        assert set(correct) == set(test)



class TestCheckContrast:
    fin = ('p', 't', 'k', 'b', 'd', 'g', 'f', 's', 'ʃ', 'h', 'm', 'n', 'ŋ', 'r', 'l', 'j','ʋ' )
    hawaiian = ('m', 'n', 'p', 'k', 'ʔ', 'h', 'w', 'l')

    # def test_one(self):
    #     x = piv.PhonFeats(ini.connect(),('v', 'z', 'ʒ', 'ð'),TestCheckContrast.fin)
    #     notcorrect = ['dorsal', 'back', 'spread_gl', 'strident', 'nasal', 'labiodental', 'front']
    #     test = x.min_feats()
    #     assert set(notcorrect) != set(test)
    def test_two(self):
        x = piv.PhonFeats(ini.connect(),('v', 'z', 'ʒ', 'ð'),TestCheckContrast.hawaiian)
        correct = False # [n] and [m] will have the same specification
        x.compute_inventory_dict()
        test = x.check_contrast(['back', 'continuant', 'lat', 'delayed_release', 'nasal'])
        assert correct == test
