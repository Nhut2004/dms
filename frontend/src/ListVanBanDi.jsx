import React, { useEffect, useState } from 'react';
import { PaperClipOutlined } from '@ant-design/icons';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { Card, Table, Button, Space, Tag, message, Popconfirm, Input } from 'antd';

const { Search } = Input;
const BASE_URL = 'http://localhost:8000';

const ListVanBanDi = () => {
    const navigate = useNavigate();
    const [data, setData] = useState([]);
    const [loading, setLoading] = useState(false);
    const [searchText, setSearchText] = useState('');

    const getAuthHeaders = () => {
        const token = localStorage.getItem('access_token');
        return { Authorization: `Bearer ${token}` };
    };

    const fetchVanBanDi = async () => {
        setLoading(true);
        try {
            const response = await axios.get(`${BASE_URL}/api/van-ban-di/`, { headers: getAuthHeaders() });
            setData(response.data || []);
        } catch (error) {
            message.error('Không thể tải danh sách văn bản đi.');
        } finally {
            setLoading(false);
        }
    };

    const handleDelete = async (id) => {
        try {
            await axios.delete(`${BASE_URL}/api/van-ban-di/${id}`, { headers: getAuthHeaders() });
            message.success('Đã xóa văn bản thành công!');
            fetchVanBanDi();
        } catch (error) {
            message.error('Lỗi khi xóa văn bản. Vui lòng thử lại!');
        }
    };

    useEffect(() => {
        fetchVanBanDi();
    }, []);

    const filteredData = data.filter((item) =>
        (item.so_ky_hieu || '').toLowerCase().includes(searchText.toLowerCase()) ||
        (item.trich_yeu || '').toLowerCase().includes(searchText.toLowerCase())
    );

    const columns = [
        { title: 'Số ký hiệu', dataIndex: 'so_ky_hieu', key: 'so_ky_hieu', width: 180 },
        { title: 'Trích yếu', dataIndex: 'trich_yeu', key: 'trich_yeu', ellipsis: true, render: (text) => text || '--' },
        { title: 'Mã hồ sơ', dataIndex: 'ma_ho_so', key: 'ma_ho_so', width: 180, render: (value) => value ? <Tag color="blue">{value}</Tag> : <Tag color="default">--</Tag> },
        {
            title: 'Tệp đính kèm',
            key: 'tep_dinh_kems',
            width: 240,
            render: (_, record) => {
                const files = record.tep_dinh_kems || [];
                if (!files.length) return <Tag color="default">--</Tag>;
                return (
                    <Space size="small" wrap>
                        {files.map((file) => {
                            const normalizedPath = file.duong_dan.replaceAll('\\', '/');
                            const fileUrl = normalizedPath.startsWith('/') ? `http://localhost:8000${normalizedPath}` : `http://localhost:8000/${normalizedPath}`;
                            return (
                                <a key={file.id} href={fileUrl} target="_blank" rel="noreferrer" style={{ display: 'inline-flex', alignItems: 'center', gap: 4 }}>
                                    <PaperClipOutlined />
                                    {file.ten_file}
                                </a>
                            );
                        })}
                    </Space>
                );
            }
        },
        {
            title: 'Hành động',
            key: 'action',
            width: 180,
            render: (_, record) => (
                <Space size="middle">
                    <Button type="link" onClick={() => navigate(`/sua-van-ban/${record.id}`)}>Xem/Sửa</Button>
                    <Popconfirm title="Xóa văn bản đi" description="Bạn có chắc chắn muốn xóa văn bản này không?" onConfirm={() => handleDelete(record.id)} okText="Có, xóa đi" cancelText="Hủy">
                        <Button type="link" danger>Xóa</Button>
                    </Popconfirm>
                </Space>
            )
        }
    ];

    return (
        <Card
            title="Danh sách Văn bản đi"
            extra={
                <Space>
                    <Search
                        placeholder="Tìm theo số ký hiệu, trích yếu..."
                        allowClear
                        onSearch={(value) => setSearchText(value)}
                        onChange={(e) => setSearchText(e.target.value)}
                        style={{ width: 300 }}
                    />
                    <Button type="primary" onClick={() => navigate('/them-van-ban')}>Thêm mới</Button>
                </Space>
            }
        >
            <Table rowKey="id" columns={columns} dataSource={filteredData} loading={loading} pagination={{ pageSize: 8 }} />
        </Card>
    );
};
export default ListVanBanDi;