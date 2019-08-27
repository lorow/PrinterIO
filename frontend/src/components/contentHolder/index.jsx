import React from 'react';
import PageTitle from '../pageTitle'
import Sidebar from '../sidebarContainer';
import Routes from '../../utils/routes';
import { Route, Switch } from 'react-router-dom';
import { TransitionGroup , Transition } from 'react-transition-group';
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

      <div className="contentHolder__page__space">
        <Route render={ ({ location }) => {
          const { key } = location;
          const routes = Routes()

          return (
            <TransitionGroup>
              <Transition
                key={key}
                appear={true}
                onEnter={ ( node ) => {console.log("enters", node)}}
                onExit={ ( node ) => {console.log("exits", node)}}
                timeout={{ enter:750, exit:150 }}
              >
                <Switch location={location}>
                  {routes.map( ({ path, Component }) => (<Route key={path} exact path={path} component={Component}/>) )}
                </Switch>
              </Transition>
            </TransitionGroup>
          )
        }} />
      </div>
    </section>
  )
}