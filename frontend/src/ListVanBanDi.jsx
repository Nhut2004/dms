import React, { useEffect, useState } from 'react';
import { PaperClipOutlined } from '@ant-design/icons';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { Table, Button, Spin, Space, Input, Modal, Form, DatePicker, InputNumber, Select, message, Popconfirm, Row, Col, Upload, Tooltip, Tag, Card } from 'antd';
const { Search } = Input;
const BASE_URL = 'http://localhost:8000';

const ListVanBanDi = () => {
    const navigate = useNavigate();
    const [data, setData] = useState([]);
    const [loading, setLoading] = useState(false);
    const [searchText, setSearchText] = useState('');

    // 1. State phân trang
    const [pagination, setPagination] = useState({
        current: 1,
        pageSize: 10,
        total: 0,
    });

    const getAuthHeaders = () => {
        const token = localStorage.getItem('access_token');
        return { Authorization: `Bearer ${token}` };
    };

    // 2. Hàm fetchData mới: Nhận page, size và keyword
    const fetchVanBanDi = async (page = 1, size = 10, keyword = '') => {
        setLoading(true);
        try {
            const response = await axios.get(`${BASE_URL}/api/van-ban-di/`, {
                headers: getAuthHeaders(),
                params: { page, size, keyword }
            });
            setData(response.data.data || []);
            setPagination(prev => ({
                ...prev,
                current: page,
                total: response.data.total
            }));
        } catch (error) {
            message.error('Không thể tải danh sách văn bản đi.');
        } finally {
            setLoading(false);
        }
    };

    const handleTableChange = (paginationConfig) => {
        fetchVanBanDi(paginationConfig.current, paginationConfig.pageSize, searchText);
    };

    const handleSearch = (value) => {
        setSearchText(value);
        fetchVanBanDi(1, pagination.pageSize, value);
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

    const handleUpdateStatus = async (id, newStatus) => {
        try {
            await axios.put(`${BASE_URL}/api/van-ban-di/${id}/trang-thai`,
                { trang_thai: newStatus },
                { headers: getAuthHeaders() }
            );
            message.success('Cập nhật trạng thái thành công!');
            fetchVanBanDi();
        } catch (error) {
            message.error('Lỗi khi cập nhật trạng thái!');
        }
    };


    useEffect(() => {
        fetchVanBanDi(pagination.current, pagination.pageSize);
    }, []);

    const filteredData = data.filter((item) =>
        (item.so_ky_hieu || '').toLowerCase().includes(searchText.toLowerCase()) ||
        (item.trich_yeu || '').toLowerCase().includes(searchText.toLowerCase())
    );

    const columns = [
        {
            title: 'Trạng thái',
            dataIndex: 'trang_thai',
            key: 'trang_thai',
            width: 140,
            render: (text) => {
                let color = 'default';
                if (text === 'DRAFT') color = 'default';
                if (text === 'PENDING_APPROVAL') color = 'warning';
                if (text === 'APPROVED') color = 'blue';
                if (text === 'PUBLISHED') color = 'success';
                if (text === 'REVOKED') color = 'error';
                return <Tag color={color}>{text || 'DRAFT'}</Tag>;
            }
        },
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
            width: 250, // Nới rộng ra một chút để chứa các nút
            render: (_, record) => (
                <Space size="middle" wrap>
                    {/* LUỒNG NGHIỆP VỤ: Ẩn/Hiện nút theo Trạng thái */}

                    {/* 1. Nếu là DRAFT -> Hiện nút Trình duyệt */}
                    {(!record.trang_thai || record.trang_thai === 'DRAFT') && (
                        <Button type="primary" size="small" onClick={() => handleUpdateStatus(record.id, 'PENDING_APPROVAL')}>
                            Trình duyệt
                        </Button>
                    )}

                    {/* 2. Nếu là PENDING_APPROVAL -> Hiện nút Phê duyệt / Từ chối */}
                    {record.trang_thai === 'PENDING_APPROVAL' && (
                        <>
                            <Button type="primary" size="small" style={{ backgroundColor: '#1890ff' }} onClick={() => handleUpdateStatus(record.id, 'APPROVED')}>
                                Phê duyệt
                            </Button>
                            <Button type="default" danger size="small" onClick={() => handleUpdateStatus(record.id, 'DRAFT')}>
                                Từ chối
                            </Button>
                        </>
                    )}

                    {/* 3. Nếu là APPROVED -> Hiện nút Phát hành */}
                    {record.trang_thai === 'APPROVED' && (
                        <Button type="primary" size="small" style={{ backgroundColor: '#52c41a' }} onClick={() => handleUpdateStatus(record.id, 'PUBLISHED')}>
                            Phát hành
                        </Button>
                    )}

                    {/* 4. Nếu là PUBLISHED -> Hiện nút Thu hồi */}
                    {record.trang_thai === 'PUBLISHED' && (
                        <Popconfirm title="Lý do thu hồi..." description="Bạn có chắc chắn muốn thu hồi văn bản này?" onConfirm={() => handleUpdateStatus(record.id, 'REVOKED')}>
                            <Button type="primary" danger size="small">Thu hồi</Button>
                        </Popconfirm>
                    )}

                    {/* NÚT CƠ BẢN (XEM/SỬA/XÓA) */}
                    <Button type="link" size="small" onClick={() => navigate(`/sua-van-ban/${record.id}`)}>Xem</Button>

                    {/* Chỉ cho xóa khi còn là Bản nháp */}
                    {(!record.trang_thai || record.trang_thai === 'DRAFT') && (
                        <Popconfirm title="Xóa văn bản đi" onConfirm={() => handleDelete(record.id)}>
                            <Button type="link" danger size="small">Xóa</Button>
                        </Popconfirm>
                    )}
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
                        onSearch={handleSearch}
                        style={{ width: 300 }}
                    />
                    <Button type="primary" onClick={() => navigate('/them-van-ban')}>Thêm mới</Button>
                </Space>
            }
        >
            <Table
                rowKey="id"
                columns={columns}
                dataSource={data}
                loading={loading}
                pagination={pagination} // Truyền config phân trang vào
                onChange={handleTableChange} // Bắt sự kiện đổi trang
                scroll={{ x: 'max-content' }}
            />
        </Card>
    );
};
export default ListVanBanDi;