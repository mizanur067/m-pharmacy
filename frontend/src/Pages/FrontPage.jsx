import React from 'react';
import { Route, Routes, BrowserRouter } from 'react-router-dom';

import Home from './Home';
import USerSignUp from './USerSignUp';
import UserLogin from './UserLogin';
import StaffLogin from './StaffLogin';
import StaffSignUp from './StaffSignUp';

const FrontPage = () => {
  return (
    <BrowserRouter>
      <Routes>
        <Route path='/' element={<Home />} />
        <Route path='/user-signup' element={<USerSignUp />} />
        <Route path='/user-login' element={<UserLogin />} />
        <Route path='/staff-login' element={<StaffLogin />} />
        <Route path='/staff-signup' element={<StaffSignUp />} />
      </Routes>
    </BrowserRouter>
  );
};

export default FrontPage;