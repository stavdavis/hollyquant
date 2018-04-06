import React from 'react';
import {connect} from 'react-redux';
import {Route, withRouter} from 'react-router-dom';

import MainNavBar from './nav-bar';
import LandingPage from './landing-page';
import Post1 from './post1';
import './app.css';

export class App extends React.Component {
    //DON'T FORGET to put a _redirects file in the public folder
    render() {
        return (
            <div className="app">
                <MainNavBar />
                <div className="main-post-area">
                    <Route exact path="/" component={Post1} />
                </div>
            </div>
        );
    }
}

const mapStateToProps = state => ({
});

// Deal with update blocking - https://reacttraining.com/react-router/web/guides/dealing-with-update-blocking
export default withRouter(connect(mapStateToProps)(App));
