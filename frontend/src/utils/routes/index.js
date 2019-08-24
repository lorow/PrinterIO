export default function Routes(){
  return (
    [
      { 
        path: '/',
        site_name: 'Dashboard',
        classes: ['dashboard', 'sideBarLink'],
        active_class: 'dashboard--active sideBarLink--active',
        Component: null
      },
      { 
        path: '/spools',
        site_name: 'Filaments',
        classes: ['filament', 'sideBarLink'],
        active_class: 'filament--active sideBarLink--active',
        Component: null
      },
      { 
        path: '/models',
        site_name: 'Models',
        classes: ['model', 'sideBarLink'],
        active_class: 'model--active sideBarLink--active',
        Component: null
      },
      { 
        path: '/queues',
        site_name: 'Queues',
        classes: ['queue', 'sideBarLink'],
        active_class: 'queue--active sideBarLink--active',
        Component: null
      },
      { 
        path: '/printers',
        site_name: 'Printers',
        classes: ['printer', 'sideBarLink'],
        active_class: 'printer--active sideBarLink--active',
        Component: null
      },
      { 
        path: '/tasks',
        site_name: 'Tasks',
        classes: ['task', 'sideBarLink'],
        active_class: 'task--active sideBarLink--active',
        Component: null
      },
      { 
        path: '/results',
        site_name: 'Results',
        classes: ['result', 'sideBarLink'],
        active_class: 'result--active sideBarLink--active',
        Component: null
      },
    ]
  )
}
