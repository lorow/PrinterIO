import React from 'react';
import Routes from '../../utils/routes';
import { useDispatch } from 'react-redux';
import { setTitle } from '../../actions/'
import SidebarLink from '../sidebarLink'
import './style.scss';

export default function Sidebar(props){

  const routes = Routes();

  const dispatch = useDispatch()

  const handleClick = pageName => {
    dispatch(setTitle(pageName));
  }

  return(
    <ul className="Sidebar">
      {routes.map( ({path, site_name, classes, active_class}) => ( 
        <li>
          <SidebarLink link={path} site_name={site_name} classes={ classes.join("\n") } active_class={active_class} handleClickFunc={handleClick}/>
        </li>
      ) )}
    </ul>
  )
}