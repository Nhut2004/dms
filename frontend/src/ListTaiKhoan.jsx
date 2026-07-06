import React, { useState, useEffect } from 'react';
import { Card, Table, Button, Input, Space, Tag, Tooltip, Popconfirm, Modal, Form, Select, message } from 'antd';
import { PlusOutlined, EditOutlined, DeleteOutlined, UserOutlined, LockOutlined } from '@ant-design/icons';
import axios from 'axios';

// Đã thêm BASE_URL để gọi đúng cổng Backend
const BASE_URL = 'http://localhost:8000';

const ListTaiKhoan = () => {
    const [data, setData] = useState([]);
    const [vaiTros, setVaiTros] = useState([]);
    const [canBos, setCanBos] = useState([]);
    const [loading, setLoading] = useState(false);
    const [modalVisible, setModalVisible] = useState(false);
    const [editingId, setEditingId] = useState(null);
    const [form] = Form.useForm();

    // Lấy quyền từ localStorage để ẩn/hiện nút hành động chuẩn xác
    const userRoles = JSON.parse(localStorage.getItem('user_roles') || '[]');
    const canEditMasterData = userRoles.includes('ADMIN');

    // Cấu hình Header cho Axios
    const getAuthHeaders = () => {
        const token = localStorage.getItem('access_token');
        return { Authorization: `Bearer ${token}` };
    };

    // Gọi 3 API khi load trang
    const fetchData = async () => {
        setLoading(true);
        try {
            const headers = getAuthHeaders();
            const [tkRes, vtRes, cbRes] = await Promise.all([
                axios.get(`${BASE_URL}/api/tai-khoan/`, { headers }),
                axios.get(`${BASE_URL}/api/tai-khoan/vai-tro`, { headers }),
                axios.get(`${BASE_URL}/api/can-bo/`, { headers })
            ]);
            setData(tkRes.data);
            setVaiTros(vtRes.data);
            setCanBos(cbRes.data);
        } catch (error) {
            message.error('Lỗi tải dữ liệu!');
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => { fetchData(); }, []);

    // Xử lý Mở Modal Thêm/Sửa
    const handleOpenModal = (record = null) => {
        setEditingId(record ? record.id : null);
        form.resetFields();
        if (record) {
            form.setFieldsValue({
                ten_dang_nhap: record.ten_dang_nhap,
                can_bo_id: record.can_bo_id,
                vai_tro_ids: record.vai_tros?.map(v => v.id) || [],
                mat_khau: undefined // Không load mật khẩu cũ
            });
        }
        setModalVisible(true);
    };

    // Xử lý Submit Form
    const handleSubmit = async () => {
        try {
            const values = await form.validateFields();
            const headers = getAuthHeaders();

            if (editingId) {
                // Tính năng PUT (Sửa) - Sẽ báo lỗi 405 vì Backend chưa viết hàm PUT, nhưng cứ để sẵn form
                if (!values.mat_khau) delete values.mat_khau;
                await axios.put(`${BASE_URL}/api/tai-khoan/${editingId}`, values, { headers });
                message.success('Cập nhật thành công!');
            } else {
                // Tính năng POST (Thêm mới)
                await axios.post(`${BASE_URL}/api/tai-khoan/`, values, { headers });
                message.success('Tạo tài khoản thành công!');
            }
            setModalVisible(false);
            fetchData();
        } catch (info) {
            if (info.errorFields) message.error('Vui lòng điền đầy đủ thông tin bắt buộc!');
            else if (info.response && info.response.data.detail) {
                message.error(info.response.data.detail); // Hiển thị lỗi trùng tên đăng nhập từ Backend
            }
        }
    };

    // Xử lý Xóa
    const handleDelete = async (id) => {
        try {
            await axios.delete(`${BASE_URL}/api/tai-khoan/${id}`, { headers: getAuthHeaders() });
            message.success('Xóa thành công!');
            fetchData();
        } catch (error) {
            // Hiển thị lỗi từ Backend (ví dụ: lỗi không được tự xóa mình)
            if (error.response && error.response.data.detail) {
                message.error(error.response.data.detail);
            } else {
                message.error('Lỗi khi xóa tài khoản!');
            }
        }
    };

    // Cấu hình Cột Bảng
    const columns = [
        { title: 'ID', dataIndex: 'id', key: 'id', width: 60 },
        { title: 'Tên đăng nhập', dataIndex: 'ten_dang_nhap', key: 'ten_dang_nhap' },
        { title: 'Trạng thái', dataIndex: 'trang_thai', key: 'trang_thai', render: v => <Tag color={v === 'ACTIVE' ? 'green' : 'red'}>{v}</Tag> },
        {
            title: 'Vai trò', dataIndex: 'vai_tros', key: 'vai_tros',
            render: (vai_tros) => vai_tros?.map(v => <Tag color="blue" key={v.id}>{v.ten_vai_tro}</Tag>)
        },
        {
            title: 'Hành động', key: 'action', width: 120, align: 'center',
            render: (_, record) => canEditMasterData ? (
                <Space size="small">
                    <Tooltip title="Sửa"><Button type="link" icon={<EditOutlined />} onClick={() => handleOpenModal(record)} /></Tooltip>
                    <Popconfirm title="Xóa tài khoản này?" onConfirm={() => handleDelete(record.id)}>
                        <Tooltip title="Xóa"><Button type="link" danger icon={<DeleteOutlined />} /></Tooltip>
                    </Popconfirm>
                </Space>
            ) : null
        }
    ];

    return (
        <Card>
            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 16 }}>
                <Input.Search placeholder="Tìm kiếm tài khoản..." style={{ width: 300 }} allowClear />
                {canEditMasterData && (
                    <Button type="primary" icon={<PlusOutlined />} onClick={() => handleOpenModal()}>Thêm mới</Button>
                )}
            </div>

            <Table rowKey="id" columns={columns} dataSource={data} loading={loading} scroll={{ x: 700 }} pagination={{ pageSize: 10 }} />

            <Modal title={editingId ? "Sửa Tài khoản" : "Thêm Tài khoản"} open={modalVisible} onOk={handleSubmit} onCancel={() => setModalVisible(false)}>
                <Form form={form} layout="vertical">
                    <Form.Item name="ten_dang_nhap" label="Tên đăng nhập" rules={[{ required: true, message: 'Bắt buộc nhập!' }]}>
                        <Input prefix={<UserOutlined />} />
                    </Form.Item>
                    <Form.Item name="mat_khau" label="Mật khẩu" rules={editingId ? [] : [{ required: true, message: 'Bắt buộc nhập mật khẩu!' }]}>
                        <Input.Password prefix={<LockOutlined />} placeholder={editingId ? "Để trống nếu không đổi" : ""} />
                    </Form.Item>
                    <Form.Item name="can_bo_id" label="Cán bộ sở hữu">
                        <Select showSearch optionFilterProp="children" placeholder="Chọn cán bộ" allowClear>
                            {canBos.map(cb => <Select.Option key={cb.id} value={cb.id}>{cb.ho_ten || `Cán bộ ID: ${cb.id}`}</Select.Option>)}
                        </Select>
                    </Form.Item>
                    <Form.Item name="vai_tro_ids" label="Vai trò" rules={[{ required: true, message: 'Chọn ít nhất 1 vai trò!' }]}>
                        <Select mode="multiple" placeholder="Chọn vai trò">
                            {vaiTros.map(vt => <Select.Option key={vt.id} value={vt.id}>{vt.ten_vai_tro}</Select.Option>)}
                        </Select>
                    </Form.Item>
                </Form>
            </Modal>
        </Card>
    );
};

export default ListTaiKhoan;