import React from 'react'
import { useNavigate } from 'react-router-dom'
import './CCS/Header.css'
const Header = () => {
     const navigate = useNavigate();
    return (
        <header className="header_mpharmacy">
            <div
                className="header_logo_mpharmacy"
                onClick={() => navigate('/')}
                style={{ cursor: 'pointer' }}
            >
                <span className="header_icon_mpharmacy">♡</span>
                <h2>
                    m-<span>pharmacy</span>
                </h2>
            </div>

            <nav className="header_nav_mpharmacy">
                <button onClick={() => navigate('/user-login')}>
                    Login
                </button>

                <button
                    className="header_cart_mpharmacy"
                    onClick={() => navigate('/cart')}
                >
                    <i className="fa-solid fa-cart-shopping"></i>
                    <span>Cart</span>
                </button>
            </nav>
        </header>
    )
}

export default Header