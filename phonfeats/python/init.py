import psycopg2
from configparser import ConfigParser
import phon_inv as piv



#returns connection parameters
def config(filename=r'phonfeats\\python\\init.py', section='postgresql'):
    parser = ConfigParser()
    parser.read(filename)

    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section,filename))

    return db

    
def connect():
    conn = None
    cur = None
    try:
        params = config()
        conn = psycopg2.connect(**params)

        cur = conn.cursor()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    
    return cur

def close(cur):
    if cur is not None:
        cur.close()


def main():
    cur = connect()
    nae = ('p', 't', 'k', 'ʔ', 'b', 'd', 'g', 'f', 'θ', 's', 'ʃ', 'h', 'v', 'ð', 'z', 'ʒ', 't͡ʃ', 'd͡ʒ', 'm', 'n', 'ŋ', 'l', 'ɹ', 'w', 'j', 'i', 'ɪ', 'u', 'ʊ', 'e', 'ɛ', 'ə', 'ʌ', 'ɔ', 'æ', 'ɑ')

    fin = ('p', 't', 'k', 'b', 'd', 'g', 'f', 's', 'ʃ', 'h', 'm', 'n', 'ŋ', 'r', 'l', 'j','ʋ' )
    hawaiian = ('m', 'n', 'p', 't', 'k', 'ʔ', 'h', 'w', 'v', 'l', 'ɾ', 'ɹ')
    hawaiian_s = ('m', 'n', 'p', 'k', 'ʔ', 'h', 'w', 'l')

    #TODO:
    # z = piv.PhonFeats(cur,('p', 't', 'k', 'm'),fin) this takes too long to run, but removing the m is fine?

    # x = piv.PhonFeats(cur,('p', 't', 'v'))
    # y = piv.PhonFeats(cur, ('d', 'z', 'ɮ', 'ð', 'n', 'l', 'r', 'ɹ'))
    # t = x.get_feat_labels()
    z = piv.PhonFeats(cur,('p', 't', 'k', 'g'),fin)
    z.compute_inventory_dict()
    # print(z.check_contrast(['back', 'continuant', 'lat', 'delayed_release', 'nasal', 'anterior']))
    # print(z.check_contrast(['back', 'front']))





    # print(z.min_feats())
    # print(len(z.listoftried))
    print(z.contrastive_features())
    # x = piv.PhonFeats(cur,('v', 'z', 'ʒ', 'ð'),hawaiian_s)
    # correct = False # [n] and [m] will have the same specification
    # test = x.check_contrast(['back', 'continuant', 'lat', 'delayed_release', 'nasal'])
    # print(test)
    # print(x.segment_feature_list('n'))


    close(cur)
    # y = piv.PhonFeats(cur,('p', 't', 'k', 'b', 'd', 'g', 'f', 's', 'ʃ', 'h', 'm', 'n', 'ŋ', 'r', 'l', 'j','ʋ'))
    # print(y.features_uncommon())
    # print(x.seg)
    # # print(x.dict_seg)
    # p = x.seg_feat_match(['+cons', '+son'])


    # x.features_common()
    # y = x.get_feat_labels()
    # for i in y:
    #     print(i, end=',')
    # print(x.features_uncommon())
    # y.min_feats()
    # mf.minimalFeatures(cur, ('d', 'z', 'ɮ', 'ð', 'n', 'l', 'r', 'ɹ'))
    # print(x.segment_feature_list('v'))
    # print(segmentFeatureList(cur,('p', 't', 'k', 'β', 'g')))


if __name__ == "__main__":
    main()

