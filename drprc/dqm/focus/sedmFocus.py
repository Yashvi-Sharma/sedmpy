import sys
sys.path.append('/data1/sedm/sedmpy/')
from drprc.dqm.sextractor import sextractor
from astropy.io import fits

def run_sextractor(image, outdir=""):
    """
    
    :param image: 
    :param outdir: 
    :return: 
    """

    return sextractor.run_sex(image=image, outdir=outdir)


def get_catalog_stats(cat, fields=None):
    """
    
    :param cat: 
    :return: 
    """
    stats_dict = {}

    if not fields:
        fields = ['FWHM_IMAGE', 'ELLIPTICITY']

    df = sextractor.analyze_sex_by_pandas(cat)

    stats_dict['FILE'] = cat
    stats_dict['NSOURCES'] = len(df)

    for f in fields:
        stats_dict[f] = df[f].mean()

    return stats_dict


def run_focus_loop(image_list, keyword='FOCPOS', cat_keyword='FWHM_IMAGE'):
    """
    
    :param image_list: 
    :return: 
    """
    stats_list = []
    best_focus_val = 100
    best_image = ''
    base_dir = '/data2/sedm/20181106/'
    for i in image_list:
        cat = run_sextractor(base_dir+i)
        focus_val = get_catalog_stats(cat)[cat_keyword]
        print(focus_val)
        if focus_val < best_focus_val and focus_val > 0:
            best_focus_val = focus_val
            best_image = base_dir+i

    focpos = fits.getheader(best_image)
    focpos = focpos[keyword]
    print(best_focus_val, focpos, best_image)

if __name__ == "__main__":


    flist = ['rc20181106_01_43_16.fits',
    'rc20181106_01_43_34.fits',
    'rc20181106_01_43_51.fits',
    'rc20181106_01_44_09.fits',
    'rc20181106_01_44_27.fits',
    'rc20181106_01_44_45.fits',
    'rc20181106_01_45_03.fits',
    'rc20181106_01_45_21.fits',
    'rc20181106_01_45_39.fits',
    'rc20181106_01_45_56.fits',
    'rc20181106_01_46_14.fits',
    'rc20181106_01_46_32.fits',
    'rc20181106_01_46_50.fits',
    'rc20181106_01_47_08.fits',
    'rc20181106_01_47_25.fits',
    'rc20181106_01_47_43.fits',
    'rc20181106_01_48_01.fits',
    'rc20181106_01_48_19.fits',
    'rc20181106_01_48_37.fits']
    run_focus_loop(flist)