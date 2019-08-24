const pageTitles = (state= "", action) => {
    switch(action.type) {
        
        // this should return state = provided title in the action
        case 'SET_TITLE':
            return action.text
        
        default:
            return "Dashboard"
    }
}

export default pageTitles