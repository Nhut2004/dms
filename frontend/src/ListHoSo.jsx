import React, { useState, useEffect } from 'react';
import { Tag, Table, Button, Space, Modal, Form, Input, DatePicker, InputNumber, Select, message, Popconfirm } from 'antd';
import axios from 'axios';
import dayjs from 'dayjs';

const API_URL = 'http://localhost:8000/api/ho-so/';
const BASE_URL = 'http://localhost:8000';

const getAuthHeaders = () => {
    const token = localStorage.getItem('access_token');
    return { Authorization: `Bearer ${token}` };
};

const ListHoSo = () => {
    const [data, setData] = useState([]);
    const [loading, setLoading] = useState(false);
    const [isModalVisible, setIsModalVisible] = useState(false);
    const [editingItem, setEditingItem] = useState(null);
    const [form] = Form.useForm();
    const [searchText, setSearchText] = useState('');
    const [viTriOptions, setViTriOptions] = useState([]);

    const fetchData = async () => {
        setLoading(true);
        try {
            const response = await axios.get(API_URL, { headers: getAuthHeaders() });
            setData(response.data);
        } catch (error) {
            message.error('Lỗi khi tải danh sách hồ sơ!');
        } finally {
            setLoading(false);
        }
    };

    const fetchOptions = async () => {
        try {
            // Lưu ý: Đảm bảo bạn đã có API này ở Backend. 
            // Nếu chưa có, bạn có thể tạm bỏ đoạn fetch này để tránh lỗi console
            const res = await axios.get(`${BASE_URL}/api/danh-muc-vi-tri/`, { headers: getAuthHeaders() });
            setViTriOptions(res.data.map(item => ({ label: item.ten_vi_tri, value: item.id })));
        } catch (error) {
            console.warn("Không tải được danh mục vị trí (API chưa tồn tại)");
        }
    };

    useEffect(() => {
        fetchData();
        fetchOptions();
    }, []);

    const handleAdd = () => {
        setEditingItem(null);
        form.resetFields();
        setIsModalVisible(true);
    };

    const handleEdit = (record) => {
        setEditingItem(record);
        form.setFieldsValue({
            ...record,
            ngay_bat_dau: record.ngay_bat_dau ? dayjs(record.ngay_bat_dau) : null,
            ngay_ket_thuc: record.ngay_ket_thuc ? dayjs(record.ngay_ket_thuc) : null,
        });
        setIsModalVisible(true);
    };

    const handleDelete = async (ma_ho_so) => {
        try {
            await axios.delete(`${API_URL}${ma_ho_so}`, { headers: getAuthHeaders() });
            message.success('Xóa hồ sơ thành công!');
            fetchData();
        } catch (error) {
            message.error(error.response?.data?.detail || 'Lỗi khi xóa hồ sơ!');
        }
    };

    const handleSubmit = async (values) => {
        try {
            const payload = {
                ...values,
                ngay_bat_dau: values.ngay_bat_dau ? values.ngay_bat_dau.format('YYYY-MM-DD') : null,
                ngay_ket_thuc: values.ngay_ket_thuc ? values.ngay_ket_thuc.format('YYYY-MM-DD') : null,
            };

            if (editingItem) {
                await axios.put(`${API_URL}${editingItem.ma_ho_so}`, payload, { headers: getAuthHeaders() });
                message.success('Cập nhật hồ sơ thành công!');
            } else {
                await axios.post(API_URL, payload, { headers: getAuthHeaders() });
                message.success('Tạo hồ sơ thành công!');
            }
            setIsModalVisible(false);
            fetchData();
        } catch (error) {
            message.error(error.response?.data?.detail || 'Lỗi thao tác!');
        }
    };

    const columns = [
        {
            title: 'Trạng thái',
            dataIndex: 'trang_thai',
            key: 'trang_thai',
            render: (text) => {
                let color = text === 'DANG_MO' ? 'green' : (text === 'DA_DONG' ? 'orange' : 'default');
                return <Tag color={color}>{text || 'DANG_MO'}</Tag>;
            }
        },
        { title: 'Mã hồ sơ', dataIndex: 'ma_ho_so', key: 'ma_ho_so', filteredValue: [searchText], onFilter: (value, record) => record.ma_ho_so.toLowerCase().includes(value.toLowerCase()) || record.tieu_de_ho_so.toLowerCase().includes(value.toLowerCase()) },
        { title: 'Tiêu đề hồ sơ', dataIndex: 'tieu_de_ho_so', key: 'tieu_de_ho_so' },
        { title: 'Thời hạn bảo quản', dataIndex: 'thoi_han_bao_quan', key: 'thoi_han_bao_quan' },
        { title: 'Chế độ sử dụng', dataIndex: 'che_do_su_dung', key: 'che_do_su_dung' },
        { title: 'Ngày bắt đầu', dataIndex: 'ngay_bat_dau', key: 'ngay_bat_dau' },
        { title: 'Ngày kết thúc', dataIndex: 'ngay_ket_thuc', key: 'ngay_ket_thuc' },
        {
            title: 'Hành động',
            key: 'action',
            render: (_, record) => (
                <Space size="middle">
                    <Button type="link" onClick={() => handleEdit(record)}>Sửa</Button>
                    <Popconfirm title="Chắc chắn xóa hồ sơ này?" onConfirm={() => handleDelete(record.ma_ho_so)}>
                        <Button type="link" danger>Xóa</Button>
                    </Popconfirm>
                </Space>
            ),
        },
    ];

    return (
        <div>
            <Space style={{ marginBottom: 16 }}>
                <Input.Search placeholder="Tìm kiếm Mã/Tiêu đề..." onChange={e => setSearchText(e.target.value)} style={{ width: 300 }} />
                <Button type="primary" onClick={handleAdd}>Thêm mới Hồ sơ</Button>
            </Space>

            <Table columns={columns} dataSource={data} rowKey="ma_ho_so" loading={loading} />

            <Modal title={editingItem ? "Chỉnh sửa Hồ sơ" : "Tạo mới Hồ sơ"} open={isModalVisible} onCancel={() => setIsModalVisible(false)} onOk={() => form.submit()} width={700}>
                <Form form={form} layout="vertical" onFinish={handleSubmit}>
                    <Form.Item name="ma_ho_so" label="Mã hồ sơ" rules={[{ required: true, message: 'Vui lòng nhập mã hồ sơ!' }]}>
                        <Input disabled={!!editingItem} />
                    </Form.Item>
                    <Form.Item name="tieu_de_ho_so" label="Tiêu đề hồ sơ" rules={[{ required: true, message: 'Vui lòng nhập tiêu đề!' }]}>
                        <Input />
                    </Form.Item>
                    <Form.Item name="file_notation" label="Số ký hiệu hồ sơ">
                        <Input />
                    </Form.Item>
                    <Form.Item name="file_catalog" label="Năm hình thành (VD: 2026)">
                        <InputNumber style={{ width: '100%' }} />
                    </Form.Item>
                    <Form.Item name="thoi_han_bao_quan" label="Thời hạn bảo quản">
                        <Select allowClear placeholder="Chọn thời hạn">
                            <Select.Option value="5 năm">5 năm</Select.Option>
                            <Select.Option value="10 năm">10 năm</Select.Option>
                            <Select.Option value="Vĩnh viễn">Vĩnh viễn</Select.Option>
                        </Select>
                    </Form.Item>
                    <Form.Item name="che_do_su_dung" label="Chế độ sử dụng">
                        <Select allowClear options={[{ value: 'Mở', label: 'Mở' }, { value: 'Hạn chế', label: 'Hạn chế' }, { value: 'Mật', label: 'Mật' }]} />
                    </Form.Item>

                    <Form.Item name="vi_tri_id" label="Vị trí lưu trữ">
                        <Select showSearch allowClear placeholder="Chọn vị trí" options={viTriOptions} filterOption={(input, option) => (option?.label ?? '').toLowerCase().includes(input.toLowerCase())} />
                    </Form.Item>
                    <Space style={{ width: '100%' }} direction="horizontal" size={16}>
                        <Form.Item name="ngay_bat_dau" label="Ngày bắt đầu" style={{ width: '50%' }}>
                            <DatePicker style={{ width: '100%' }} format="YYYY-MM-DD" />
                        </Form.Item>
                        <Form.Item name="ngay_ket_thuc" label="Ngày kết thúc" style={{ width: '50%' }}>
                            <DatePicker style={{ width: '100%' }} format="YYYY-MM-DD" />
                        </Form.Item>
                    </Space>
                    <Form.Item name="so_luong_trang" label="Số lượng trang" rules={[{ type: 'number', min: 0, message: 'Số trang không được âm!' }]}>
                        <InputNumber style={{ width: '100%' }} />
                    </Form.Item>
                    <Form.Item name="so_luong_van_ban" label="Số lượng văn bản" rules={[{ type: 'number', min: 0, message: 'Số lượng không được âm!' }]}>
                        <InputNumber style={{ width: '100%' }} />
                    </Form.Item>
                    <Form.Item name="nguoi_lap" label="Người lập"><Input /></Form.Item>
                    <Form.Item name="ngon_ngu" label="Ngôn ngữ"><Input /></Form.Item>
                    <Form.Item name="ghi_chu" label="Ghi chú"><Input.TextArea rows={3} /></Form.Item>
                </Form>
            </Modal>
        </div>
    );
};

export default ListHoSo;