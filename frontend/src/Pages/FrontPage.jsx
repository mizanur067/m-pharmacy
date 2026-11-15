import React from 'react';
import { Route, Routes, BrowserRouter } from 'react-router-dom';

import Home from './Home';
import USerSignUp from './USerSignUp';
import UserLogin from './UserLogin';

const FrontPage = () => {
  return (
    <BrowserRouter>
      <Routes>
        <Route path='/' element={<Home />} />
        <Route path='/user-signup' element={<USerSignUp />} />
        <Route path='/user-login' element={<UserLogin />} />
      </Routes>
    </BrowserRouter>
  );
};

export default FrontPage;