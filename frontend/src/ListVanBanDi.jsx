import React, { useEffect, useState } from 'react';
import { PaperClipOutlined } from '@ant-design/icons';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { Table, Button, Space, Input, Modal, Form, DatePicker, InputNumber, Select, message, Popconfirm, Row, Col, Upload, Tooltip, Tag, Card } from 'antd';
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
            width: 250, // Độ rộng cố định cho cột
            render: (_, record) => {
                const files = record.tep_dinh_kems || [];
                if (!files.length) return <span style={{ color: '#bfbfbf' }}>Không có file</span>;

                return (
                    // Đổi Space thành div flex column để mỗi file nằm 1 dòng cho gọn
                    <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
                        {files.map((file, i) => {
                            // Xử lý đường dẫn file (Nếu đang ở file Văn bản đi thì dùng logic URL của bạn)
                            const normalizedPath = file.duong_dan.replaceAll('\\', '/');
                            const fileUrl = normalizedPath.startsWith('/') ? `${BASE_URL}${normalizedPath}` : `${BASE_URL}/${normalizedPath}`;

                            return (
                                /* Bọc bằng Tooltip để khi di chuột vào hiện full tên */
                                <Tooltip title={file.ten_file} key={file.id || i} placement="topLeft">
                                    <a
                                        href={fileUrl}
                                        target="_blank"
                                        rel="noreferrer"
                                        style={{
                                            display: 'block',
                                            maxWidth: '220px',      // Giới hạn chiều dài tối đa
                                            whiteSpace: 'nowrap',   // Ép không cho rớt dòng
                                            overflow: 'hidden',     // Phần thừa ra sẽ bị giấu đi
                                            textOverflow: 'ellipsis'// Thêm dấu 3 chấm (...) ở cuối
                                        }}
                                    >
                                        <PaperClipOutlined style={{ marginRight: '4px' }} />
                                        {file.ten_file}
                                    </a>
                                </Tooltip>
                            );
                        })}
                    </div>
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