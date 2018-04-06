//Based on: https://github.com/hjmccain/maplyful
//IMPORTANT:
//Don't forget to import bootstraps' basic css file into the main index.html: 
//<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/latest/css/bootstrap.min.css">
//Here we've imported the actual css files (generated at https://getbootstrap.com/docs/3.3/customize/) - b/c the remote link was not stable
//see nav-bar-bootstrap.css and nav-bar-bootstrap.theme.css
import React from 'react';
import { Nav, Navbar, NavItem } from 'react-bootstrap';
import {Link} from 'react-router-dom';
import './nav-bar-bootstrap.css';
import './nav-bar-bootstrap-theme.css';
import './nav-bar.css';
import mainLogo from '../assets/main-logo.png';


export default class MainNavBar extends React.Component {
  render() {
    let rightNavLinks = (
      <Nav className="top-menu-links">
        <NavItem><Link className="navbar-app-link" to="/all-articles">All Articles</Link></NavItem>
        <NavItem><Link className="navbar-app-link" to="/about">About</Link></NavItem>
        <NavItem><Link className="navbar-app-link" to="/contact">Contact</Link></NavItem>
        <NavItem><Link className="navbar-app-link" to="/news">News</Link></NavItem>
      </Nav>
    );
    return (
      <Navbar className="navbar-app" collapseOnSelect>
        <Navbar.Header>
          <Navbar.Toggle />
          <Navbar.Brand>
            <Link className="top-logo" to="/"><img className="main-logo" src={mainLogo} alt="Site Logo" /></Link>
            <Link className="app-name" to="/"><span className="small-the-word">The<br/></span>Hollywood Quantifier</Link>
          </Navbar.Brand>
        </Navbar.Header>
        <Navbar.Collapse>
          {rightNavLinks}
        </Navbar.Collapse>
      </Navbar>
    );
  }
}