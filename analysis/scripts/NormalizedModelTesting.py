
def testToModel_onefile(file):
    from . import preprocessor as pc
    from sklearn.externals import joblib
    from vizn_ml_django.settings import BASE_DIR
    import os


    # load trained model
    clf = joblib.load(os.path.join(BASE_DIR, 'analysis/scripts/model/SVC_rbf_wt_cleaned.model'))
    data = pc.one_file_extract_and_norm_timepoints(file)
    try:
        result = clf.predict(data['array'])
    except:
        print("DATA NOT AS EXPECTED. ABORTING.")
        exit(1)

    output = {'result': result, 'skipped': data['skipped'], 'array': data['array'], 'plate': data['plate']}

    return output

