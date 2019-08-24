import React from 'react';
import PageTitle from '../pageTitle'
import Sidebar from '../sidebarContainer';
import './style.scss'

export default function ContentHolder(props){
  return(

    <section className="contentHolder">
      <div className="contentHolder__page__title">
        <PageTitle />
      </div>

      <div className="contentHolder__sidemenu">
        <Sidebar />
      </div>
    </section>

  )
}