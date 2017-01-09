
def testToModel_onefile(file):
    from . import preprocessor as pc
    from sklearn.externals import joblib
    from vizn_ml_django.settings import BASE_DIR
    import os


    # load trained model
    clf = joblib.load(os.path.join(BASE_DIR, 'analysis/scripts/model/SVC_rbf_wt_tuned_std.model'))
    scaler = joblib.load(os.path.join(BASE_DIR, 'analysis/scripts/model/scaler.model'))
    # data = pc.one_file_extract_and_norm_timepoints(file)
    data = pc.one_file_extract_and_no_norm(file)
    X = scaler.transform(data['array'])


    try:
        result = clf.predict(X)
    except:
        print("DATA NOT AS EXPECTED. ABORTING.")
        exit(1)

    output = {'result': result, 'skipped': data['skipped'], 'array': data['array'], 'plate': data['plate']}

    return output

