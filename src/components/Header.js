import React from "react"
import { Link } from 'react-router-dom';
import './Header.css';

import logo from '../images/logo.png'
import account_icon from '../images/account_circle_filled_white_24px.png'
import menu_icon from '../images/menu_white_24px.png'

import Sidebar from './Sidebar';

export default function Header() {
    const [isSidebarOpen, setSidebarOpen] = React.useState(false);

    const toggleSidebar = () => {
        setSidebarOpen(!isSidebarOpen);
    };

    return (
        <header className="header">
            <Link to="/">
            <img 
                src={logo} 
                alt="ODEUM" 
                className="header--image"
            />
            </Link>
            <img
                src={account_icon} 
                alt="account"
                className="header--account--image"
                onClick={toggleSidebar}
            />
            <img 
                src={menu_icon} 
                alt="menu"
                className="header--menu--image"
            />
            <Sidebar isOpen={isSidebarOpen} onClose={toggleSidebar} />
        </header>
    );
}