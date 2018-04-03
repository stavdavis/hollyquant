import React from 'react';
import {connect} from 'react-redux';
import {Route, withRouter} from 'react-router-dom';

// import MainNavBar from './nav-bar';
import LandingPage from './landing-page';
                // <MainNavBar />


export class App extends React.Component {
    //DON'T FORGET to put a _redirects file in the public folder
    render() {
        return (
            <div className="app">
                <Route exact path="/" component={LandingPage} />
            </div>
        );
    }
}

const mapStateToProps = state => ({
});

// Deal with update blocking - https://reacttraining.com/react-router/web/guides/dealing-with-update-blocking
export default withRouter(connect(mapStateToProps)(App));
