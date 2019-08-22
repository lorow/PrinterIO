import React, { useState } from 'react';
import './style.scss';

export default function Navbar(props){

  var username = "lorow"; // TODO add downloading of the username after authentication is implemented
  var profileImageLink = "https://placekitten.com/200/200"; // make it so that django / ngnix hosts the statics and provides the link to them

  var classNames = require('classnames');

  const [isFormActive, setFormActive] = useState(false)

  var searchFormClass = classNames({
    'navbar__search__form': true,
    'navbar__search__form--active': isFormActive 
  })

  const handleChangeInForm = (e) => {
    e.preventDefault();
    console.log(e);
  }

  return (
  <header className="navbar">
      <h1 className="navbar__title">PrinterIO</h1>
      <ul className="navbar__links" role="navigation">
        <li className="navbar__item__holder">
          <form className={searchFormClass} onChange={handleChangeInForm} onSubmit={handleChangeInForm}>
            <input type="search" name="global_search" placeholder="Search for printers, filaments or models..." />
          </form>
          <button className="navbar__button navbar__button--search" onClick={() => {setFormActive(!isFormActive)}}>
            <img src="/svg_icons/searchIcon.svg" alt="search button"/ >
          </button>
        </li>
        <li className="navbar__item__holder"><button className="navbar__button navbar__button--bell"><img src="/svg_icons/bellIcon.svg" alt="notiffication bell"/></button></li>
        <li className="navbar__item__holder navbar__item__holder--withSpacing">
          <figure className="navbar__profile">
            <figcaption className="navbar__profile__caption">Welcome back, <span>{username}!</span> </figcaption>
            <img className="navbar__profile__image" src={profileImageLink} alt={username}/>
          </figure>
        </li>
        <li className="navbar__item__holder navbar__item__holder--withSpacing"><button className="navbar__button navbar__button--action">Print something!</button></li>
      </ul>
    </header>
  )
}

