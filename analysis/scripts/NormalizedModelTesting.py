
def testToModel_onefile(file):
    import scripts.preprocessor as pc
    from sklearn.externals import joblib
    from settings import MODEL_DIR
    import os

    # load trained model
    clf = joblib.load(os.path.join(MODEL_DIR, 'SVC_rbf.model'))
    data = pc.one_file_extract_and_norm_timepoints(file)
    try:
        result = clf.predict(data['array'])
    except:
        print("DATA NOT AS EXPECTED. ABORTING.")
        exit(1)

    output = {'result': result, 'skipped': data['skipped'], 'array': data['array'], 'plate': data['plate']}

    return output

