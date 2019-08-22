import React from 'react';
import { useSelector } from 'react-redux';
import './style.scss'

export default function PageTitle (props){

    const title = useSelector(state => state.pageTitles)

    return(
        <h2 className="PageTitle">{title}</h2>
    )
}