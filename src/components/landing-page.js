import React from 'react';
import {connect} from 'react-redux';
// import {Redirect} from 'react-router-dom';
import './landing-page.css';

export function LandingPage(props) {
    return (
        <div className="landing-page">
            <div className="test-section">
                <h1><br/><br/><br/><br/><br/><br/><br/>Test Section of Landing Page</h1>
            </div>
        </div>
    );
}

const mapStateToProps = state => ({
});

export default connect(mapStateToProps)(LandingPage);
