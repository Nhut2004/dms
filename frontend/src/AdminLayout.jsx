import React, { useState } from 'react';
import { Layout, Menu, Button, message } from 'antd';
import {
    DashboardOutlined,
    FileTextOutlined,
    SendOutlined,
    FolderOpenOutlined,
    ApartmentOutlined,
    LogoutOutlined
} from '@ant-design/icons';
import { Outlet, useNavigate, useLocation } from 'react-router-dom';

const { Sider, Header, Content } = Layout;

const menuItems = [
    { key: '/dashboard', icon: <DashboardOutlined />, label: 'Bảng điều khiển' },
    { key: '/van-ban-den', icon: <FileTextOutlined />, label: 'Quản lý Văn bản đến' },
    { key: '/van-ban-di', icon: <SendOutlined />, label: 'Quản lý Văn bản đi' },
    { key: '/ho-so', icon: <FolderOpenOutlined />, label: 'Quản lý Hồ sơ' },
    { key: '/co-quan', icon: <ApartmentOutlined />, label: 'Quản lý Cơ quan' }
];

const AdminLayout = () => {
    const navigate = useNavigate();
    const location = useLocation();
    const [collapsed, setCollapsed] = useState(false);

    const handleLogout = () => {
        localStorage.removeItem('access_token');
        message.success('Đăng xuất thành công');
        navigate('/login');
    };

    return (
        <Layout style={{ minHeight: '100vh' }}>
            <Sider
                collapsible
                collapsed={collapsed}
                onCollapse={setCollapsed}
                width={240}
                style={{
                    background: '#001529'
                }}
            >
                <div
                    style={{
                        height: 64,
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        color: '#fff',
                        fontWeight: 700,
                        fontSize: collapsed ? 16 : 18,
                        borderBottom: '1px solid rgba(255,255,255,0.08)'
                    }}
                >
                    {collapsed ? 'DMS' : 'DMS Admin'}
                </div>

                <Menu
                    theme="dark"
                    mode="inline"
                    selectedKeys={[location.pathname]}
                    items={menuItems}
                    onClick={({ key }) => navigate(key)}
                />
            </Sider>

            <Layout>
                <Header
                    style={{
                        background: '#fff',
                        padding: '0 24px',
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'space-between',
                        borderBottom: '1px solid #f0f0f0'
                    }}
                >
                    <div style={{ fontSize: 16, fontWeight: 600 }}>
                        {menuItems.find((item) => item.key === location.pathname)?.label || 'Bảng điều khiển'}
                    </div>

                    <Button
                        type="text"
                        icon={<LogoutOutlined />}
                        onClick={handleLogout}
                    >
                        Đăng xuất
                    </Button>
                </Header>

                <Content
                    style={{
                        margin: 16,
                        padding: 24,
                        background: '#f5f7fb',
                        minHeight: 280
                    }}
                >
                    <Outlet />
                </Content>
            </Layout>
        </Layout>
    );
};

export default AdminLayout;
