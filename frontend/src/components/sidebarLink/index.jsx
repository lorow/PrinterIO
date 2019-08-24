import React from 'react';
import { NavLink } from 'react-router-dom'

export default function SidebarLink(props){
    return(
      <NavLink exact to={props.link} alt={props.site_name} className={props.classes} activeClassName={props.active_class} 
        onClick={(e) => {
          props.handleClickFunc(props.site_name);
        }}
      />
    )
}