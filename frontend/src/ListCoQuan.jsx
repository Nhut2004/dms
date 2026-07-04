import React, { useEffect, useState } from 'react';
import { Table, Button, Space, Input, Modal, Form, message, Popconfirm, Tooltip, Card } from 'antd';
import { PlusOutlined, EditOutlined, DeleteOutlined } from '@ant-design/icons';
import axios from 'axios';

const BASE_URL = 'http://localhost:8000';
const API_URL = `${BASE_URL}/api/co-quan/`;

const getAuthHeaders = () => {
    const token = localStorage.getItem('access_token');
    return { Authorization: `Bearer ${token}` };
};

const ListCoQuan = () => {
    const [data, setData] = useState([]);
    const [loading, setLoading] = useState(false);
    const [searchText, setSearchText] = useState('');
    const [isModalVisible, setIsModalVisible] = useState(false);
    const [editingItem, setEditingItem] = useState(null);
    const [form] = Form.useForm();

    const [pagination, setPagination] = useState({
        current: 1,
        pageSize: 10,
        total: 0,
    });

    const fetchData = async (page = 1, size = 10, keyword = searchText) => {
        setLoading(true);
        try {
            const response = await axios.get(API_URL, {
                headers: getAuthHeaders(),
                params: { page, size, keyword }
            });
            setData(response.data || []);
            setPagination(prev => ({
                ...prev,
                current: page,
                pageSize: size,
                total: response.data?.length || 0
            }));
        } catch (error) {
            message.error('Lỗi khi tải danh sách cơ quan!');
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchData(pagination.current, pagination.pageSize);
    }, []);

    const handleTableChange = (paginationConfig) => {
        fetchData(paginationConfig.current, paginationConfig.pageSize, searchText);
    };

    const handleSearch = (value) => {
        setSearchText(value);
        fetchData(1, pagination.pageSize, value);
    };

    const handleAdd = () => {
        setEditingItem(null);
        form.resetFields();
        setIsModalVisible(true);
    };

    const handleEdit = (record) => {
        setEditingItem(record);
        form.setFieldsValue(record);
        setIsModalVisible(true);
    };

    const handleDelete = async (id) => {
        try {
            await axios.delete(`${API_URL}${id}`, { headers: getAuthHeaders() });
            message.success('Xóa cơ quan thành công!');
            fetchData(pagination.current, pagination.pageSize, searchText);
        } catch (error) {
            message.error(error.response?.data?.detail || 'Lỗi khi xóa cơ quan!');
        }
    };

    const handleSubmit = async (values) => {
        try {
            if (editingItem) {
                await axios.put(`${API_URL}${editingItem.id}`, values, { headers: getAuthHeaders() });
                message.success('Cập nhật cơ quan thành công!');
            } else {
                await axios.post(API_URL, values, { headers: getAuthHeaders() });
                message.success('Thêm mới cơ quan thành công!');
            }

            setIsModalVisible(false);
            form.resetFields();
            fetchData(pagination.current, pagination.pageSize, searchText);
        } catch (error) {
            const errorMsg = error.response?.data?.detail || 'Lỗi hệ thống khi lưu cơ quan!';
            message.error(errorMsg);
        }
    };

    const filteredData = data.filter((item) => {
        if (!searchText) return true;
        const keyword = searchText.toLowerCase();
        return (
            (item.ten_co_quan || '').toLowerCase().includes(keyword) ||
            (item.organ_id || '').toLowerCase().includes(keyword)
        );
    });

    const columns = [
        {
            title: 'Mã định danh (Organ ID)',
            dataIndex: 'organ_id',
            key: 'organ_id',
            width: 180,
            render: (text) => <strong style={{ color: '#1677ff' }}>{text}</strong>
        },
        {
            title: 'Tên cơ quan / tổ chức',
            dataIndex: 'ten_co_quan',
            key: 'ten_co_quan',
            render: (text) => <strong>{text}</strong>
        },
        {
            title: 'Địa chỉ',
            dataIndex: 'dia_chi',
            key: 'dia_chi',
            width: 320,
            ellipsis: true,
            render: (text) => (
                <Tooltip title={text || '---'} placement="topLeft" color="blue">
                    <span>{text || '---'}</span>
                </Tooltip>
            )
        },
        {
            title: 'Hành động',
            key: 'action',
            align: 'center',
            width: 140,
            render: (_, record) => (
                <Space size="small" style={{ whiteSpace: 'nowrap' }}>
                    <Tooltip title="Chỉnh sửa">
                        <Button
                            type="primary"
                            icon={<EditOutlined />}
                            style={{ backgroundColor: '#52c41a', borderColor: '#52c41a' }}
                            onClick={() => handleEdit(record)}
                        />
                    </Tooltip>
                    <Tooltip title="Xóa">
                        <Popconfirm title="Bạn có chắc muốn xóa cơ quan này?" onConfirm={() => handleDelete(record.id)}>
                            <Button type="primary" danger icon={<DeleteOutlined />} />
                        </Popconfirm>
                    </Tooltip>
                </Space>
            )
        }
    ];

    return (
        <Card
            title="Quản lý Cơ quan"
            extra={
                <Space>
                    <Input.Search
                        placeholder="Tìm theo tên hoặc mã cơ quan"
                        allowClear
                        onSearch={handleSearch}
                        style={{ width: 300 }}
                    />
                    <Button type="primary" icon={<PlusOutlined />} onClick={handleAdd}>Thêm mới</Button>
                </Space>
            }
        >
            <Table
                rowKey="id"
                columns={columns}
                dataSource={filteredData}
                loading={loading}
                pagination={pagination}
                onChange={handleTableChange}
                scroll={{ x: 'max-content' }}
            />

            <Modal
                title={editingItem ? 'Cập nhật cơ quan' : 'Thêm mới cơ quan'}
                open={isModalVisible}
                onOk={() => form.submit()}
                onCancel={() => {
                    setIsModalVisible(false);
                    form.resetFields();
                }}
                okText="Lưu"
                cancelText="Hủy"
            >
                <Form layout="vertical" form={form} onFinish={handleSubmit}>
                    <Form.Item label="Mã định danh (Organ ID)" name="organ_id" rules={[{ required: true, message: 'Vui lòng nhập mã định danh' }]}>
                        <Input disabled={!!editingItem} />
                    </Form.Item>
                    <Form.Item label="Tên cơ quan / tổ chức" name="ten_co_quan" rules={[{ required: true, message: 'Vui lòng nhập tên cơ quan' }]}>
                        <Input />
                    </Form.Item>
                    <Form.Item label="Địa chỉ" name="dia_chi">
                        <Input.TextArea rows={3} />
                    </Form.Item>
                </Form>
            </Modal>
        </Card>
    );
};

export default ListCoQuan;
