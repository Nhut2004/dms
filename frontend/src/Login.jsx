import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Button, Card, Form, Input, message } from 'antd';
import axios from 'axios';
import logo from './assets/CTU_logo.png';

const Login = () => {
    const navigate = useNavigate();
    const onFinish = async (values) => {
        const params = new URLSearchParams();
        params.append('username', values.username);
        params.append('password', values.password);

        try {
            const response = await axios.post(
                'http://localhost:8000/api/auth/login',
                params,
                {
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded'
                    }
                }
            );

            if (response.status === 200) {
                localStorage.setItem('access_token', response.data.access_token);
                message.success('Đăng nhập thành công!');

                navigate('/');
            }
        } catch (error) {
            message.error('Sai tài khoản hoặc mật khẩu!');
        }
    };

    return (
        <div
            style={{
                position: 'relative', /* Thêm thuộc tính này để làm gốc tọa độ cho logo */
                minHeight: '100vh',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                background: '#f5f7fb'
            }}
        >
            {/* Gắn logo góc trên bên trái */}
            <img
                src={logo}
                alt="Logo CTU"
                style={{
                    position: 'absolute',
                    top: '24px',
                    left: '24px',
                    height: '60px', /* Bạn có thể tăng giảm số này để chỉnh độ to nhỏ của logo */
                    objectFit: 'contain'
                }}
            />

            <Card
                style={{
                    width: 420,
                    borderRadius: 12,
                    boxShadow: '0 8px 24px rgba(0, 0, 0, 0.08)'
                }}
            >
                <div style={{ textAlign: 'center', marginBottom: 24 }}>
                    <h2 style={{ marginBottom: 8 }}>Đăng nhập</h2>
                    <p style={{ margin: 0, color: '#8c8c8c' }}>
                        Hệ thống quản lý tài liệu điện tử
                    </p>
                </div>

                <Form layout="vertical" onFinish={onFinish}>
                    <Form.Item
                        label="Tên đăng nhập"
                        name="username"
                        rules={[{ required: true, message: 'Vui lòng nhập tên đăng nhập' }]}
                    >
                        <Input size="large" placeholder="Nhập tên đăng nhập" />
                    </Form.Item>

                    <Form.Item
                        label="Mật khẩu"
                        name="password"
                        rules={[{ required: true, message: 'Vui lòng nhập mật khẩu' }]}
                    >
                        <Input.Password size="large" placeholder="Nhập mật khẩu" />
                    </Form.Item>

                    <Form.Item>
                        <Button type="primary" htmlType="submit" size="large" block>
                            Đăng nhập
                        </Button>
                    </Form.Item>
                </Form>
            </Card>
        </div>
    );
};

axios.interceptors.response.use(
    (response) => response,
    (error) => {
        if (error.response && error.response.status === 401) {
            message.error('Phiên đăng nhập đã hết hạn. Vui lòng đăng nhập lại!');
            localStorage.removeItem('access_token');
            window.location.href = '/login';
        }
        return Promise.reject(error);
    }
);

export default Login;