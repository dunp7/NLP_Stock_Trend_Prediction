@contextmanager
def timer(title):
    '''
    This function is used to calculate the time it takes to run a function
    '''

    t0 = time.time()
    yield
    print("{} - done in {:.0f}s".format(title, time.time() - t0))

    def __init__(self, folder=r'dataset', train_size=0.8, random_state=42):
            X_train, X_test, y_train, y_test = self.get_train_test_splits(
                folder=folder, train_size=train_size, random_state=random_state)
            self.X_train = X_train
            self.X_test = X_test
            self.y_train = y_train
            self.y_test = y_test

            
def model_selection(self, model='Random Forest Optuna', param=None, verbose=True, n_trials=100, distance='euclidean', version='normal', plot=False, method='both',num_prediction = 5):
    with timer(model):
        model_name, model_func = self.model_mapping(model)
        if 'Optuna' in model_name:
            param = self.optimize_and_train(model_func, n_trials=n_trials)
            print('Best parameters:', param)
            if plot:
                _, _,self.predicted_class = self.train_and_report(model_func, param, verbose=False)
                self.plot_ml_based(method = method)
            gc.collect()

    
        acc, report,self.predicted_class = self.train_and_report(model_func, param, verbose)
        self.plot_ml_based(method = method)

        print(f'Accuracy of {model_name}: {acc}')
        if verbose:
            print('Classification Report:\n', report)
        gc.collect()

    return acc, report

def model_mapping(self, model):
    mapping = {
        'Logistic Regression': LogisticRegression,
        'Random Forest': RandomForestClassifier,
        'LightGBM': LGBMClassifier,
        'CatBoost': CatBoostClassifier,
        'XGBoost': XGBClassifier,
        'Random Forest Optuna': RandomForestClassifier,
        'LightGBM Optuna': LGBMClassifier,
        'CatBoost Optuna': CatBoostClassifier,
        'XGBoost Optuna': XGBClassifier,
    }
        return model, mapping[model]

def train_and_report(self, model, param, verbose=False):
        clf = model(**param)
        clf.fit(self.X_train, self.y_train)
        y_pred = clf.predict(self.X_test)
        accuracy = accuracy_score(self.y_test, y_pred)
        report = classification_report(
            self.y_test, y_pred, zero_division=0) if verbose else None
        return accuracy, report, y_pred

    def optimize_and_train(self, model, n_trials=100):
        param_search_space = self.get_param_search_space(model)
        return self.optimize_and_train_inner(model, param_search_space, n_trials)

    def suggest_parameter(self, trial, param_name, param_type, param_range):
        if param_type == 'int':
            return trial.suggest_int(name=param_name, low=param_range[0], high=param_range[1])
        elif param_type == 'float':
            return trial.suggest_float(name=param_name, low=param_range[0], high=param_range[1], log=param_range[2])
        elif param_type == 'categorical':
            return trial.suggest_categorical(name=param_name, choices=param_range)
        else:
            raise ValueError(f"Unsupported parameter type: {param_type}")

    def objective(self, trial, param_search_space, model):
        param = {key: self.suggest_parameter(
            trial, key, value[0], value[1]) for key, value in param_search_space.items()}
        clf = model(**param)
        return cross_val_score(clf, self.X_train, self.y_train, n_jobs=-1, cv=3).mean()

    def optimize_and_train_inner(self, model, param_search_space, n_trials=100):
        study = optuna.create_study(direction='maximize')

        def objective_wrapper(trial):
            return self.objective(trial, param_search_space, model)

        study.optimize(objective_wrapper, n_trials=n_trials)
        print('Number of finished trials:', len(study.trials))
        print('Best trial:', study.best_trial.params)

        return study.best_trial.params

    def get_param_search_space(self, model):
    param_search_spaces = {
        LogisticRegression: {
            'C': ('float', (1e-2, 1e2, 'log')),
            'penalty': ('categorical', ['l1', 'l2']),
            'solver': ('categorical', ['liblinear', 'newton-cg', 'lbfgs', 'sag', 'saga'])
        },
        RandomForestClassifier: {
            'n_estimators': ('int', (200, 500)),
            'max_depth': ('int', (10, 50)),
            'min_samples_split': ('int', (2, 10)),
            'min_samples_leaf': ('int', (1, 10)),
            'bootstrap': ('categorical', [True, False])
        },
        LGBMClassifier: {
            'num_leaves': ('int', (31, 127)),
            'learning_rate': ('float', (0.01, 0.1)),
            'n_estimators': ('int', (100, 500)),
            'max_depth': ('int', (-1, 10))
        },
        CatBoostClassifier: {
            'iterations': ('int', (500, 1000)),
            'learning_rate': ('float', (0.01, 0.1)),
            'depth': ('int', (3, 10)),
            'l2_leaf_reg': ('float', (1, 10))
        },
        XGBClassifier: {
            'max_depth': ('int', (3, 10)),
            'learning_rate': ('float', (0.01, 0.1)),
            'n_estimators': ('int', (100, 500)),
            'gamma': ('float', (0, 10))
        }
    }
    return param_search_spaces.get(model, {})

    def test_n_components(min_components=20, max_components=160, step=20, model='Random Forest', folder=r'dataset', train_size=0.8, param=None, verbose=True, n_trials=100, distance='euclidean', version='normal', plot=False, method='both', random_state=42, pca_method='pca',num_prediction = 5):
    scores = {
        'Accuracy': [],
        'Precision': [],
        'Recall': [],
        'F1-Score': []
    }

    for i in range(min_components, max_components + step, step):

            with timer('Model Selection'):
                acc, report = fdm.model_selection(
                    model=model, param=param, verbose=verbose, n_trials=n_trials, distance=distance, version=version, plot=plot, method=method, num_prediction = num_prediction)
                gc.collect()

            # Collect scores for each component
            scores['Accuracy'].append(acc)
            report = report.split('\n\n')[2].split('\n')[
                2].split('      ')[1:-1]
            scores['Precision'].append(float(report[0]))
            scores['Recall'].append(float(report[1]))
            scores['F1-Score'].append(float(report[2]))

    # Create a single plot for all scores
    components_range = range(min_components, max_components + step, step)
    plt.figure(figsize=(10, 7))
    plt.plot(components_range, scores['Accuracy'], label='Accuracy')
    plt.plot(components_range, scores['Precision'], label='Precision')
    plt.plot(components_range, scores['Recall'], label='Recall')
    plt.plot(components_range, scores['F1-Score'], label='F1-Score')
    plt.show()

    def main(model, folder=r'.\dataset', train_size=0.8, param=None,
            verbose=True, n_components=150, n_trials=20, distance='euclidean', version='normal', plot=False, method='both', num_prediction = 5, random_state=42, pca_method='pca'):
    '''
    This function is used to run the entire project

    Parameters:
    model (str): Model to be used
    folder (str): Folder containing the dataset
    train_size (int): Number of images to be used for training
    param (dict): Parameters for the model
    verbose (bool): Whether to print the classification report or not
    n_components (int): Number of components to be used for feature extraction
    n_trials (int): Number of trials for Optuna
    distance (str): Distance metric to be used
    version (str): Version of the distance metric to be used
    '''

    with timer('Model Selection'):
        fdm.model_selection(model=model, param=param,
                            verbose=verbose, n_trials=n_trials, distance=distance, version=version, plot=plot, method=method, num_prediction = num_prediction)
        gc.collect()


if __name__ == '__main__':
    '''Để test n component 1 loạt các model với param có vẻ ổn'''
    best_params = {
    'Logistic Regression': {'C': 1.0, 'penalty': 'l2', 'solver': 'liblinear'},
    'Random Forest': {'n_estimators': 100, 'max_depth': None, 'min_samples_split': 2, 'min_samples_leaf': 1, 'bootstrap': True},
    'LightGBM': {'num_leaves': 31, 'learning_rate': 0.1, 'n_estimators': 100},
    'CatBoost': {'iterations': 1000, 'learning_rate': 0.1, 'depth': 6, 'l2_leaf_reg': 3},
    'XGBoost': {'max_depth': 3, 'learning_rate': 0.1, 'n_estimators': 100}
}
    for i in list(best_params.keys()):
        test_n_components(min_components=20, max_components=150, step=20, model=i, folder=r'.\dataset', train_size=0.8,
                          param=best_params[i], verbose=True, n_trials=20, random_state=42, pca_method='pca', plot=False)

    '''Để tunning 1 loạt các model'''
    list_model_optuna = ['Logistic Regression', 'Random Forest', 'LightGBM',
                         'CatBoost', 'XGBoost']
    for i in list_model_optuna:
        main(model=i, folder=r'.\dataset', train_size=0.8,
             n_components=50, random_state=42, verbose=False, plot=False, n_trials=50)

