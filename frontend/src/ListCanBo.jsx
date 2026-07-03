import React, { useEffect, useState } from 'react';
import { Table, Button, Space, Input, Modal, Form, Select, message, Popconfirm, Tooltip, Tag, Card } from 'antd';
import { PlusOutlined, EditOutlined, DeleteOutlined } from '@ant-design/icons';
import axios from 'axios';

const BASE_URL = 'http://localhost:8000';
const API_URL = `${BASE_URL}/api/can-bo/`;

const getAuthHeaders = () => {
    const token = localStorage.getItem('access_token');
    return { Authorization: `Bearer ${token}` };
};

const ListCanBo = () => {
    const [data, setData] = useState([]);
    const [loading, setLoading] = useState(false);
    const [searchText, setSearchText] = useState('');
    const [isModalVisible, setIsModalVisible] = useState(false);
    const [editingRecord, setEditingRecord] = useState(null);
    const [coQuanOptions, setCoQuanOptions] = useState([]);
    const [form] = Form.useForm();

    const [pagination, setPagination] = useState({
        current: 1,
        pageSize: 10,
        total: 0,
    });

    const fetchCoQuanOptions = async () => {
        try {
            const response = await axios.get(`${BASE_URL}/api/co-quan/`, { headers: getAuthHeaders() });
            const options = (response.data || []).map(item => ({ label: item.ten_co_quan, value: item.id }));
            setCoQuanOptions(options);
        } catch (error) {
            console.warn('Không tải được danh sách cơ quan:', error.message);
        }
    };

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
            message.error('Lỗi khi tải danh sách cán bộ!');
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchCoQuanOptions();
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
        setEditingRecord(null);
        form.resetFields();
        setIsModalVisible(true);
    };

    const handleEdit = (record) => {
        setEditingRecord(record);
        form.setFieldsValue(record);
        setIsModalVisible(true);
    };

    const handleDelete = async (id) => {
        try {
            await axios.delete(`${API_URL}${id}`, { headers: getAuthHeaders() });
            message.success('Xóa cán bộ thành công!');
            fetchData(pagination.current, pagination.pageSize, searchText);
        } catch (error) {
            message.error(error.response?.data?.detail || 'Lỗi khi xóa cán bộ!');
        }
    };

    const handleSubmit = async (values) => {
        try {
            if (editingRecord) {
                await axios.put(`${API_URL}${editingRecord.id}`, values, { headers: getAuthHeaders() });
                message.success('Cập nhật cán bộ thành công!');
            } else {
                await axios.post(API_URL, values, { headers: getAuthHeaders() });
                message.success('Thêm mới cán bộ thành công!');
            }

            setIsModalVisible(false);
            form.resetFields();
            fetchData(pagination.current, pagination.pageSize, searchText);
        } catch (error) {
            const errorMsg = error.response?.data?.detail || 'Lỗi hệ thống khi lưu cán bộ!';
            message.error(errorMsg);
        }
    };

    const filteredData = data.filter((item) => {
        if (!searchText) return true;
        const keyword = searchText.toLowerCase();
        return (item.ho_ten || '').toLowerCase().includes(keyword);
    });

    const columns = [
        { title: 'ID', dataIndex: 'id', key: 'id', width: 70, align: 'center' },
        {
            title: 'Họ và tên',
            dataIndex: 'ho_ten',
            key: 'ho_ten',
            render: (text) => <strong style={{ color: '#1677ff' }}>{text}</strong>
        },
        {
            title: 'Chức vụ',
            dataIndex: 'chuc_vu',
            key: 'chuc_vu',
            width: 220,
            render: (text) => {
                if (!text) return <span style={{ color: '#8c8c8c' }}>--- </span>;
                let color = 'default';
                if (text.toLowerCase().includes('giám đốc') || text.toLowerCase().includes('lãnh đạo')) color = 'red';
                else if (text.toLowerCase().includes('chánh văn phòng')) color = 'purple';
                else if (text.toLowerCase().includes('chuyên viên')) color = 'blue';
                return <Tag color={color}>{text}</Tag>;
            }
        },
        {
            title: 'Đơn vị/Cơ quan',
            dataIndex: 'co_quan_id',
            key: 'co_quan_id',
            width: 260,
            render: (id) => {
                const coQuan = coQuanOptions.find(item => item.value === id);
                return <span>{coQuan?.label || '---'}</span>;
            }
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
                        <Popconfirm title="Bạn có chắc muốn xóa cán bộ này?" onConfirm={() => handleDelete(record.id)}>
                            <Button type="primary" danger icon={<DeleteOutlined />} />
                        </Popconfirm>
                    </Tooltip>
                </Space>
            )
        }
    ];

    return (
        <Card
            title="Quản lý Cán bộ"
            extra={
                <Space>
                    <Input.Search
                        placeholder="Tìm theo tên cán bộ"
                        allowClear
                        onSearch={handleSearch}
                        style={{ width: 280 }}
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
                title={editingRecord ? 'Cập nhật cán bộ' : 'Thêm mới cán bộ'}
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
                    <Form.Item label="Họ và tên" name="ho_ten" rules={[{ required: true, message: 'Vui lòng nhập họ và tên' }]}>
                        <Input />
                    </Form.Item>
                    <Form.Item label="Chức vụ" name="chuc_vu">
                        <Select
                            placeholder="Chọn hoặc nhập chức vụ"
                            allowClear
                            options={[
                                { label: 'Lãnh đạo', value: 'Lãnh đạo' },
                                { label: 'Giám đốc', value: 'Giám đốc' },
                                { label: 'Chánh văn phòng', value: 'Chánh văn phòng' },
                                { label: 'Chuyên viên', value: 'Chuyên viên' },
                                { label: 'Phó phòng', value: 'Phó phòng' }
                            ]}
                        />
                    </Form.Item>
                    <Form.Item label="Đơn vị/Cơ quan" name="co_quan_id" rules={[{ required: true, message: 'Vui lòng chọn cơ quan' }]}>
                        <Select options={coQuanOptions} placeholder="Chọn cơ quan" />
                    </Form.Item>
                </Form>
            </Modal>
        </Card>
    );
};

export default ListCanBo;
