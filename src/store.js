import {createStore, combineReducers} from 'redux';
import generalReducers from './reducers/general-reducers';

const store = createStore(
    combineReducers({
        generalReducers: generalReducers
        // reducerNameInStore: importedReducerName,
        // reducerNameInStore: importedReducerName
    })
);

export default store;
