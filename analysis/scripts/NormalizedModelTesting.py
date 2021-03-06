
def testToModel_onefile(file):
    from . import preprocessor as pc
    from sklearn.externals import joblib
    from vizn_ml_django.settings import BASE_DIR
    import os

    # load trained model
    clf = joblib.load(os.path.join(BASE_DIR, 'analysis/scripts/model/new_model_Jan_31_2016.model'))
    data = pc.one_file_extract_and_no_norm(file)
    test_data = data['array']
    test_data = pc.process_for_prediction(test_data)

    try:
        result = clf.predict(test_data)
    except:
        print("DATA NOT AS EXPECTED. ABORTING.")
        exit(1)

    output = {'result': result, 'skipped': data['skipped'], 'array': data['array'], 'plate': data['plate']}

    return output

