import React, { useState, useEffect } from 'react';
import { Table, Button, Space, Input, Modal, Form, DatePicker, InputNumber, Select, message, Popconfirm, Row, Col, Upload } from 'antd';
import { EditOutlined, DeleteOutlined, PlusOutlined, SearchOutlined, InboxOutlined, PaperClipOutlined } from '@ant-design/icons';
import axios from 'axios';
import dayjs from 'dayjs';

const { Dragger } = Upload;
const BASE_URL = 'http://localhost:8000';

const ListVanBanDen = () => {
    const [data, setData] = useState([]);
    const [loading, setLoading] = useState(false);
    const [searchText, setSearchText] = useState('');
    const [isModalVisible, setIsModalVisible] = useState(false);
    const [editingRecord, setEditingRecord] = useState(null);
    const [form] = Form.useForm();

    // State mới để chứa File tải lên
    const [fileList, setFileList] = useState([]);

    const [coQuanOptions, setCoQuanOptions] = useState([]);
    const [danhMucOptions, setDanhMucOptions] = useState([]);
    const [hoSoOptions, setHoSoOptions] = useState([]);

    const apiUrl = `${BASE_URL}/api/van-ban-den/`;

    const getAuthHeaders = () => {
        const token = localStorage.getItem('access_token');
        return { Authorization: `Bearer ${token}` };
    };

    const fetchOptions = async () => {
        try {
            const [coQuanRes, danhMucRes, hoSoRes] = await Promise.all([
                axios.get(`${BASE_URL}/api/co-quan/`, { headers: getAuthHeaders() }),
                axios.get(`${BASE_URL}/api/danh-muc/`, { headers: getAuthHeaders() }),
                axios.get(`${BASE_URL}/api/ho-so/`, { headers: getAuthHeaders() })
            ]);
            setCoQuanOptions((coQuanRes.data || []).map(item => ({ label: item.ten_co_quan, value: item.id })));
            setDanhMucOptions((danhMucRes.data || []).map(item => ({ label: item.ten_loai_vb, value: item.id })));
            setHoSoOptions((hoSoRes.data || []).map(item => ({ label: item.ma_ho_so, value: item.ma_ho_so })));
        } catch (error) {
            console.error('Lỗi tải danh mục');
        }
    };

    const fetchData = async () => {
        setLoading(true);
        try {
            const response = await axios.get(apiUrl, { headers: getAuthHeaders() });
            setData(Array.isArray(response.data) ? response.data : []);
        } catch (error) {
            setData([]);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchOptions();
        fetchData();
    }, []);

    const handleDelete = async (id) => {
        try {
            await axios.delete(`${BASE_URL}/api/van-ban-den/${id}`, { headers: getAuthHeaders() });
            message.success('Xóa văn bản đến thành công!');
            fetchData();
        } catch (error) {
            message.error('Lỗi khi xóa văn bản đến!');
        }
    };

    const handleSubmit = async (values) => {
        try {
            const payload = {
                ...values,
                ngay_den: values.ngay_den ? values.ngay_den.format('YYYY-MM-DD') : null,
                ngay_ban_hanh: values.ngay_ban_hanh ? values.ngay_ban_hanh.format('YYYY-MM-DD') : null,
                han_giai_quyet: values.han_giai_quyet ? values.han_giai_quyet.format('YYYY-MM-DD') : null,
            };

            let vanBanId = null;

            if (editingRecord) {
                const putUrl = `${BASE_URL}/api/van-ban-den/${editingRecord.id}`;
                await axios.put(putUrl, payload, { headers: getAuthHeaders() });
                vanBanId = editingRecord.id;
                message.success('Cập nhật nội dung thành công!');
            } else {
                const res = await axios.post(apiUrl, payload, { headers: getAuthHeaders() });
                vanBanId = res.data.id; // Chộp ngay cái ID vừa được DB cấp
                message.success('Thêm mới văn bản thành công!');
            }

            // --- NẾU CÓ CHỌN FILE THÌ ĐẨY LÊN BẰNG API RIÊNG ---
            if (fileList.length > 0 && vanBanId) {
                const formData = new FormData();
                fileList.forEach(file => {
                    // Lấy file vật lý từ Antd Upload
                    formData.append('files', file.originFileObj || file);
                });

                await axios.post(`${BASE_URL}/api/van-ban-den/${vanBanId}/upload`, formData, {
                    headers: {
                        ...getAuthHeaders(),
                        'Content-Type': 'multipart/form-data'
                    }
                });
                message.success('Đã tải lên tệp đính kèm!');
            }

            setIsModalVisible(false);
            setFileList([]); // Quét sạch file list để chuẩn bị cho lần tạo mới tiếp theo
            fetchData();
        } catch (error) {
            message.error('Lỗi khi lưu văn bản!');
        }
    };

    const showEditModal = (record) => {
        setEditingRecord(record);
        form.setFieldsValue({
            ...record,
            ngay_den: record.ngay_den ? dayjs(record.ngay_den) : null,
            ngay_ban_hanh: record.ngay_ban_hanh ? dayjs(record.ngay_ban_hanh) : null,
            han_giai_quyet: record.han_giai_quyet ? dayjs(record.han_giai_quyet) : null,
        });
        setFileList([]); // Tạm thời clear khi bấm Sửa
        setIsModalVisible(true);
    };

    const showCreateModal = () => {
        setEditingRecord(null);
        form.resetFields();
        form.setFieldsValue({ ngon_ngu: 'Tiếng Việt' });
        setFileList([]);
        setIsModalVisible(true);
    };

    const filteredData = data.filter((item) => {
        if (!searchText) return true;
        const lowerSearch = searchText.toLowerCase();
        return (
            String(item.so_den).toLowerCase().includes(lowerSearch) ||
            (item.ky_hieu && item.ky_hieu.toLowerCase().includes(lowerSearch)) ||
            (item.trich_yeu && item.trich_yeu.toLowerCase().includes(lowerSearch))
        );
    });

    const columns = [
        { title: 'Số đến', dataIndex: 'so_den', width: 90 },
        { title: 'Ký hiệu', dataIndex: 'ky_hieu', width: 120 },
        { title: 'Ngày đến', dataIndex: 'ngay_den', render: (text) => text ? dayjs(text).format('DD/MM/YYYY') : '', width: 110 },
        {
            title: 'Cơ quan ban hành',
            dataIndex: 'co_quan_ban_hanh_id',
            render: (id) => coQuanOptions.find(opt => opt.value === id)?.label || 'Chưa xác định',
            width: 200
        },
        { title: 'Trích yếu', dataIndex: 'trich_yeu', ellipsis: true },
        // CỘT HIỂN THỊ FILE ĐÍNH KÈM
        {
            title: 'File đính kèm',
            key: 'tep_dinh_kems',
            width: 220,
            render: (_, record) => {
                const files = record.tep_dinh_kems || [];
                if (!files.length) return <span style={{ color: '#bfbfbf' }}>Không có file</span>;
                return (
                    <Space size="small" wrap>
                        {files.map((f, i) => (
                            <a key={i} href={`${BASE_URL}/${f.duong_dan.replaceAll('\\', '/')}`} target="_blank" rel="noreferrer">
                                <PaperClipOutlined /> {f.ten_file}
                            </a>
                        ))}
                    </Space>
                );
            }
        },
        {
            title: 'Hành động',
            key: 'action',
            width: 120,
            render: (_, record) => (
                <Space size="middle">
                    <Button type="primary" icon={<EditOutlined />} onClick={() => showEditModal(record)} />
                    <Popconfirm title="Bạn có chắc muốn xóa?" onConfirm={() => handleDelete(record.id)}>
                        <Button type="primary" danger icon={<DeleteOutlined />} />
                    </Popconfirm>
                </Space>
            ),
        },
    ];

    return (
        <div style={{ padding: '24px', background: '#fff', borderRadius: '8px' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '16px' }}>
                <Input placeholder="Tìm kiếm theo Số đến, Ký hiệu, Trích yếu..." prefix={<SearchOutlined />} value={searchText} onChange={(e) => setSearchText(e.target.value)} style={{ width: 400 }} />
                <Button type="primary" icon={<PlusOutlined />} onClick={showCreateModal}>Thêm mới</Button>
            </div>

            <Table columns={columns} dataSource={filteredData} rowKey="id" loading={loading} pagination={{ pageSize: 10 }} scroll={{ x: 1200 }} />

            <Modal title={editingRecord ? "Cập nhật Văn bản đến" : "Thêm mới Văn bản đến"} open={isModalVisible} onCancel={() => setIsModalVisible(false)} onOk={() => form.submit()} okText="Lưu" cancelText="Hủy" width={850}>
                <Form form={form} layout="vertical" onFinish={handleSubmit}>
                    <Row gutter={16}>
                        <Col span={12}>
                            <Form.Item name="so_den" label="Số đến" rules={[{ required: true }]}><InputNumber style={{ width: '100%' }} /></Form.Item>
                            <Form.Item name="ky_hieu" label="Ký hiệu"><Input placeholder="Ví dụ: 123/QĐ-UBND" /></Form.Item>
                            <Form.Item name="ngay_den" label="Ngày đến" rules={[{ required: true }]}><DatePicker style={{ width: '100%' }} format="DD/MM/YYYY" /></Form.Item>
                            <Form.Item name="ngay_ban_hanh" label="Ngày ban hành"><DatePicker style={{ width: '100%' }} format="DD/MM/YYYY" /></Form.Item>
                            <Form.Item name="ma_loai_vb_id" label="Loại văn bản" rules={[{ required: true }]}>
                                <Select showSearch options={danhMucOptions} placeholder="Chọn loại văn bản" filterOption={(input, option) => (option?.label ?? '').toLowerCase().includes(input.toLowerCase())} />
                            </Form.Item>
                            <Form.Item name="co_quan_ban_hanh_id" label="Cơ quan ban hành">
                                <Select showSearch options={coQuanOptions} placeholder="Chọn cơ quan ban hành" filterOption={(input, option) => (option?.label ?? '').toLowerCase().includes(input.toLowerCase())} />
                            </Form.Item>
                            <Form.Item name="trich_yeu" label="Trích yếu" rules={[{ required: true }]}><Input.TextArea rows={3} /></Form.Item>
                        </Col>
                        <Col span={12}>
                            <Form.Item name="ngon_ngu" label="Ngôn ngữ"><Input /></Form.Item>
                            <Form.Item name="so_trang" label="Số trang"><InputNumber style={{ width: '100%' }} min={1} /></Form.Item>
                            <Form.Item name="ho_ten_nguoi_ky" label="Họ tên người ký"><Input placeholder="Ví dụ: Nguyễn Văn A" /></Form.Item>
                            <Form.Item name="chuc_vu_nguoi_ky" label="Chức vụ người ký"><Input placeholder="Ví dụ: Giám đốc" /></Form.Item>
                            <Form.Item name="don_vi_nhan" label="Nơi nhận nội bộ"><Input placeholder="Phòng Hành chính, Phòng Kế toán..." /></Form.Item>
                            <Form.Item name="do_khan" label="Mức độ khẩn">
                                <Select allowClear placeholder="Chọn mức độ khẩn">
                                    <Select.Option value={1}>Thường</Select.Option><Select.Option value={2}>Khẩn</Select.Option><Select.Option value={3}>Thượng khẩn</Select.Option><Select.Option value={4}>Hỏa tốc</Select.Option>
                                </Select>
                            </Form.Item>
                            <Form.Item name="han_giai_quyet" label="Hạn giải quyết"><DatePicker style={{ width: '100%' }} format="DD/MM/YYYY" /></Form.Item>
                            <Form.Item name="ma_ho_so" label="Đưa vào hồ sơ">
                                <Select showSearch options={hoSoOptions} placeholder="Chọn mã hồ sơ lưu trữ" allowClear filterOption={(input, option) => (option?.label ?? '').toLowerCase().includes(input.toLowerCase())} />
                            </Form.Item>
                        </Col>
                    </Row>

                    {/* KHUNG KÉO THẢ FILE CỦA ANT DESIGN */}
                    <Row style={{ marginTop: '16px' }}>
                        <Col span={24}>
                            <h4 style={{ marginBottom: 8 }}>Tệp đính kèm</h4>
                            <Dragger
                                multiple
                                fileList={fileList}
                                beforeUpload={() => false} // Chặn không cho Antd tự upload, để code tự kiểm soát
                                onChange={({ fileList: newFileList }) => setFileList(newFileList)}
                            >
                                <p className="ant-upload-drag-icon"><InboxOutlined /></p>
                                <p className="ant-upload-text">Kéo thả hoặc click để chọn tệp (PDF, Word...)</p>
                            </Dragger>
                        </Col>
                    </Row>
                </Form>
            </Modal>
        </div>
    );
};

export default ListVanBanDen;