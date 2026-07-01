// frontend/src/Dashboard.jsx
import React, { useState, useEffect } from 'react';
import { Row, Col, Card, Statistic, Progress, Tag, Spin, Typography, message, Button } from 'antd';
import { FileTextOutlined, InboxOutlined, FolderOpenOutlined, ArrowUpOutlined } from '@ant-design/icons';
import axios from 'axios';

const { Title, Text } = Typography;
const BASE_URL = 'http://localhost:8000';

const Dashboard = () => {
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(false);

    const getAuthHeaders = () => {
        const token = localStorage.getItem('access_token');
        return { Authorization: `Bearer ${token}` };
    };

    const fetchData = async () => {
        setLoading(true);
        try {
            const response = await axios.get(`${BASE_URL}/api/thong-ke/tong-quan`, { headers: getAuthHeaders() });
            setData(response.data);
        } catch (error) {
            console.error("Lỗi tải dữ liệu thống kê");
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchData();
    }, []);

    if (loading || !data) return <div style={{ textAlign: 'center', padding: '50px' }}><Spin size="large" /></div>;

    // Hàm tính tỷ lệ phần trăm an toàn (tránh chia cho 0)
    const calcPercent = (value, total) => total === 0 ? 0 : Math.round((value / total) * 100);

    return (
        <div style={{ padding: '24px', background: '#f5f5f5', minHeight: '100vh' }}>
            <Title level={3} style={{ marginBottom: '24px' }}> Tổng quan Hệ thống Quản lý Tài liệu</Title>

            {/* KHỐI 1: 3 THẺ CARD TỔNG QUAN */}
            <Row gutter={[24, 24]} style={{ marginBottom: '32px' }}>
                <Col xs={24} sm={12} lg={8}>
                    <Card
                        hoverable
                        style={{ borderTop: '4px solid #1890ff' }}
                    >
                        <Statistic
                            title="Tổng Văn bản đi"
                            value={data.van_ban_di.tong}
                            prefix={<FileTextOutlined style={{ color: '#1890ff' }} />}
                            suffix={<Text type="secondary" style={{ fontSize: '14px' }}>văn bản</Text>}
                        />
                    </Card>
                </Col>
                <Col xs={24} sm={12} lg={8}>
                    <Card
                        hoverable
                        style={{ borderTop: '4px solid #52c41a' }}
                    >
                        <Statistic
                            title="Tổng Văn bản đến"
                            value={data.van_ban_den.tong}
                            prefix={<InboxOutlined style={{ color: '#52c41a' }} />}
                            suffix={<Text type="secondary" style={{ fontSize: '14px' }}>văn bản</Text>}
                        />
                    </Card>
                </Col>
                <Col xs={24} sm={12} lg={8}>
                    <Card
                        hoverable
                        style={{ borderTop: '4px solid #faad14' }}
                    >
                        <Statistic
                            title="Tổng Hồ sơ lưu trữ"
                            value={data.ho_so.tong}
                            prefix={<FolderOpenOutlined style={{ color: '#faad14' }} />}
                            suffix={<Text type="secondary" style={{ fontSize: '14px' }}>hồ sơ</Text>}
                        />
                    </Card>
                </Col>
            </Row>

            {/* KHỐI 2: CHI TIẾT TRẠNG THÁI */}
            <Row gutter={[24, 24]}>
                {/* Văn bản đi */}
                <Col xs={24} lg={8}>
                    <Card title="Trạng thái Văn bản đi" bordered={false}>
                        <div style={{ marginBottom: '16px' }}>
                            <Text>Nháp (DRAFT)</Text>
                            <Progress percent={calcPercent(data.van_ban_di.trang_thai.DRAFT, data.van_ban_di.tong)} size="small" status="normal" />
                        </div>
                        <div style={{ marginBottom: '16px' }}>
                            <Text>Chờ duyệt (PENDING)</Text>
                            <Progress percent={calcPercent(data.van_ban_di.trang_thai.PENDING_APPROVAL, data.van_ban_di.tong)} size="small" status="active" strokeColor="#faad14" />
                        </div>
                        <div style={{ marginBottom: '16px' }}>
                            <Text>Đã phát hành (PUBLISHED)</Text>
                            <Progress percent={calcPercent(data.van_ban_di.trang_thai.PUBLISHED, data.van_ban_di.tong)} size="small" status="active" strokeColor="#52c41a" />
                        </div>
                        <div>
                            <Text>Đã thu hồi (REVOKED)</Text>
                            <Progress percent={calcPercent(data.van_ban_di.trang_thai.REVOKED, data.van_ban_di.tong)} size="small" status="exception" />
                        </div>
                    </Card>
                </Col>

                {/* Văn bản đến */}
                <Col xs={24} lg={8}>
                    <Card title="Trạng thái Văn bản đến" bordered={false}>
                        <div style={{ marginBottom: '16px' }}>
                            <Text>Chờ xử lý</Text>
                            <Progress percent={calcPercent(data.van_ban_den.trang_thai.CHO_XU_LY, data.van_ban_den.tong)} size="small" status="exception" />
                        </div>
                        <div style={{ marginBottom: '16px' }}>
                            <Text>Đang xử lý</Text>
                            <Progress percent={calcPercent(data.van_ban_den.trang_thai.DANG_XU_LY, data.van_ban_den.tong)} size="small" status="active" strokeColor="#1890ff" />
                        </div>
                        <div>
                            <Text>Đã xử lý</Text>
                            <Progress percent={calcPercent(data.van_ban_den.trang_thai.DA_XU_LY, data.van_ban_den.tong)} size="small" strokeColor="#52c41a" />
                        </div>
                    </Card>
                </Col>

                {/* Hồ sơ */}
                <Col xs={24} lg={8}>
                    <Card title="Trạng thái Hồ sơ" bordered={false}>
                        <div style={{ marginBottom: '16px' }}>
                            <Text>Đang mở</Text>
                            <Progress percent={calcPercent(data.ho_so.trang_thai.DANG_MO, data.ho_so.tong)} size="small" status="active" strokeColor="#1890ff" />
                        </div>
                        <div>
                            <Text>Đã đóng</Text>
                            <Progress percent={calcPercent(data.ho_so.trang_thai.DA_DONG, data.ho_so.tong)} size="small" strokeColor="#8c8c8c" />
                        </div>

                        <div style={{ marginTop: '32px', padding: '12px', background: '#f0f2f5', borderRadius: '8px' }}>
                            <Text type="secondary" style={{ display: 'block', marginBottom: '8px' }}>Phân bổ nhanh:</Text>
                            <Tag color="blue">Đang mở: {data.ho_so.trang_thai.DANG_MO}</Tag>
                            <Tag color="default">Đã đóng: {data.ho_so.trang_thai.DA_DONG}</Tag>
                        </div>
                    </Card>
                </Col>
            </Row>
        </div>
    );
};

export default Dashboard;
