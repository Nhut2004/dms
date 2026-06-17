import React, { useEffect, useState } from 'react';
import { Card, Table, Button, Space, Tag, message } from 'antd';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

const BASE_URL = 'http://localhost:8000';

const ListVanBanDi = () => {
    const navigate = useNavigate();
    const [data, setData] = useState([]);
    const [loading, setLoading] = useState(false);

    const getAuthHeaders = () => {
        const token = localStorage.getItem('access_token');
        return {
            Authorization: `Bearer ${token}`
        };
    };

    const fetchVanBanDi = async () => {
        setLoading(true);
        try {
            const response = await axios.get(`${BASE_URL}/api/van-ban-di/`, {
                headers: getAuthHeaders()
            });
            setData(response.data || []);
        } catch (error) {
            message.error('Không thể tải danh sách văn bản đi.');
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchVanBanDi();
    }, []);

    const columns = [
        {
            title: 'Số ký hiệu',
            dataIndex: 'so_ky_hieu',
            key: 'so_ky_hieu',
            width: 180
        },
        {
            title: 'Trích yếu',
            dataIndex: 'trich_yeu',
            key: 'trich_yeu',
            ellipsis: true,
            render: (text) => text || '--'
        },
        {
            title: 'Mã hồ sơ',
            dataIndex: 'ma_ho_so',
            key: 'ma_ho_so',
            width: 180,
            render: (value) =>
                value ? <Tag color="blue">{value}</Tag> : <Tag color="default">--</Tag>
        },
        {
            title: 'Hành động',
            key: 'action',
            width: 180,
            render: () => (
                <Space size="middle">
                    <Button type="link">Xem/Sửa</Button>
                    <Button type="link" danger>
                        Xóa
                    </Button>
                </Space>
            )
        }
    ];

    return (
        <Card
            title="Danh sách Văn bản đi"
            extra={
                <Button type="primary" onClick={() => navigate('/them-van-ban')}>
                    Thêm mới
                </Button>
            }
        >
            <Table
                rowKey="id"
                columns={columns}
                dataSource={data}
                loading={loading}
                pagination={{ pageSize: 8 }}
            />
        </Card>
    );
};

export default ListVanBanDi;
