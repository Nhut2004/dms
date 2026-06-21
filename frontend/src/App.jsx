import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import Login from './Login';
import AdminLayout from './AdminLayout';
import CreateVanBanDi from './CreateVanBanDi';
import ListVanBanDi from './ListVanBanDi';
// 1. Thêm import component ListVanBanDen vừa tạo
import ListVanBanDen from './ListVanBanDen';

const ProtectedRoute = ({ children }) => {
  const token = localStorage.getItem('access_token');
  if (!token) {
    return <Navigate to="/login" replace />;
  }
  return children;
};

const App = () => {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<Login />} />

        <Route
          path="/"
          element={
            <ProtectedRoute>
              <AdminLayout />
            </ProtectedRoute>
          }
        >
          <Route index element={
            <div style={{ padding: 24, fontSize: 18 }}>
              Chào mừng bạn đến với Hệ thống Quản lý tài liệu điện tử!
            </div>
          } />

          {/* Luồng Văn bản đi */}
          <Route path="van-ban-di" element={<ListVanBanDi />} />
          <Route path="them-van-ban" element={<CreateVanBanDi />} />
          <Route path="sua-van-ban/:id" element={<CreateVanBanDi />} />

          {/* Luồng Văn bản đến */}
          <Route path="van-ban-den" element={<ListVanBanDen />} />
          {/* <Route path="them-van-ban-den" element={<CreateVanBanDen />} /> */}
          {/* <Route path="sua-van-ban-den/:id" element={<CreateVanBanDen />} /> */}
        </Route>
      </Routes>
    </BrowserRouter>
  );
};

export default App;