import React, { useState, useEffect } from 'react';
import { Table, Button, Space, Input, Modal, Form, DatePicker, InputNumber, Select, message, Popconfirm, Row, Col, Upload, Tooltip, Tag } from 'antd';
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
    const [pagination, setPagination] = useState({
        current: 1,
        pageSize: 10,
        total: 0,
    });
    // State mới để chứa File tải lên
    const [fileList, setFileList] = useState([]);

    const [coQuanOptions, setCoQuanOptions] = useState([]);
    const [danhMucOptions, setDanhMucOptions] = useState([]);
    const [hoSoOptions, setHoSoOptions] = useState([]);
    const [canBoOptions, setCanBoOptions] = useState([]);
    const apiUrl = `${BASE_URL}/api/van-ban-den/`;

    const getAuthHeaders = () => {
        const token = localStorage.getItem('access_token');
        return { Authorization: `Bearer ${token}` };
    };

    const fetchOptions = async () => {
        try {
            const [coQuanRes, danhMucRes, hoSoRes, canBoRes] = await Promise.all([
                axios.get(`${BASE_URL}/api/co-quan/`, { headers: getAuthHeaders() }),
                axios.get(`${BASE_URL}/api/danh-muc/`, { headers: getAuthHeaders() }),
                axios.get(`${BASE_URL}/api/ho-so/`, { headers: getAuthHeaders() }),
                axios.get(`${BASE_URL}/api/can-bo/`, { headers: getAuthHeaders() })
            ]);
            setCoQuanOptions((coQuanRes.data || []).map(item => ({ label: item.ten_co_quan, value: item.id })));
            setDanhMucOptions((danhMucRes.data || []).map(item => ({ label: item.ten_loai_vb, value: item.id })));
            const hoSoArray = Array.isArray(hoSoRes.data) ? hoSoRes.data : (hoSoRes.data?.data || []);
            setHoSoOptions(hoSoArray.map(item => ({ label: item.ma_ho_so, value: item.ma_ho_so })));
            setCanBoOptions((canBoRes.data || []).map(item => ({
                label: `${item.ho_ten} ${item.chuc_vu ? `(${item.chuc_vu})` : ''}`,
                value: item.id
            })));
        } catch (error) {
            console.error('Lỗi tải danh mục');
        }
    };

    const fetchData = async (page = 1, size = 10, keyword = searchText) => {
        setLoading(true);
        try {
            const response = await axios.get(apiUrl, {
                headers: getAuthHeaders(),
                params: { page, size, keyword } // Gửi keyword lên Backend
            });
            setData(response.data.data || []);
            setPagination(prev => ({ ...prev, current: page, total: response.data.total }));
        } catch (error) {
            message.error('Lỗi khi tải dữ liệu!');
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchOptions();
        fetchData(pagination.current, pagination.pageSize);
    }, []);

    const handleTableChange = (paginationConfig) => {
        fetchData(paginationConfig.current, paginationConfig.pageSize);
    };

    const handleSearch = (value) => {
        setSearchText(value);
        fetchVanBanDi(1, pagination.pageSize); // Luôn gọi trang 1 khi bắt đầu tìm kiếm mới
    };

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
            // Trích xuất thông báo lỗi chi tiết (detail) mà Backend gửi về
            const errorMessage = error.response?.data?.detail || 'Lỗi hệ thống khi lưu văn bản!';

            // Có thể FastAPI trả về mảng lỗi (Validation Error)
            if (Array.isArray(errorMessage)) {
                message.error(`Dữ liệu không hợp lệ: ${errorMessage[0].msg}`);
            } else {
                message.error(errorMessage);
            }
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
        {
            title: 'Trạng thái xử lý',
            dataIndex: 'trang_thai_xu_ly',
            key: 'trang_thai_xu_ly',
            width: 150,
            render: (text) => {
                let color = text === 'CHO_XU_LY' ? 'warning' : (text === 'DANG_XU_LY' ? 'processing' : 'success');
                return <Tag color={color}>{text || 'CHO_XU_LY'}</Tag>;
            }
        },
        { title: 'Số đến', dataIndex: 'so_den', width: 90 },
        { title: 'Ký hiệu', dataIndex: 'ky_hieu', width: 130 },
        { title: 'Ngày đến', dataIndex: 'ngay_den', render: (text) => text ? dayjs(text).format('DD/MM/YYYY') : '', width: 110 },
        {
            title: 'Cơ quan ban hành',
            dataIndex: 'co_quan_ban_hanh_id',
            width: 220,
            ellipsis: true,
            render: (id) => {
                const tenCoQuan = coQuanOptions.find(opt => opt.value === id)?.label || 'Chưa xác định';
                return (
                    <Tooltip title={tenCoQuan} placement="topLeft" color="blue">
                        <span>{tenCoQuan}</span>
                    </Tooltip>
                );
            }
        },
        {
            title: 'Trích yếu',
            dataIndex: 'trich_yeu',
            width: 280,
            ellipsis: true,
            render: (text) => (
                <Tooltip title={text} placement="topLeft" color="blue">
                    <span style={{ cursor: 'pointer' }}>{text || '--'}</span>
                </Tooltip>
            )
        },
        {
            title: 'Tệp đính kèm',
            key: 'tep_dinh_kems',
            width: 220,
            render: (_, record) => {
                const files = record.tep_dinh_kems || [];
                if (!files.length) return <span style={{ color: '#bfbfbf' }}>Không có file</span>;

                return (

                    <div style={{ display: 'flex', flexDirection: 'column', gap: '4px' }}>
                        {files.map((file, i) => {
                            const normalizedPath = file.duong_dan.replaceAll('\\', '/');
                            const fileUrl = normalizedPath.startsWith('/') ? `${BASE_URL}${normalizedPath}` : `${BASE_URL}/${normalizedPath}`;

                            return (
                                <Tooltip title={file.ten_file} key={file.id || i} placement="topLeft">
                                    <a
                                        href={fileUrl}
                                        target="_blank"
                                        rel="noreferrer"
                                        style={{
                                            display: 'block',
                                            maxWidth: '200px',
                                            whiteSpace: 'nowrap',
                                            overflow: 'hidden',
                                            textOverflow: 'ellipsis'
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
            title: 'Hạn giải quyết',
            dataIndex: 'han_giai_quyet',
            width: 170,
            render: (text) => {
                if (!text) return <span style={{ color: '#bfbfbf' }}>Không có hạn</span>;

                const deadline = dayjs(text);
                const today = dayjs().startOf('day');
                const diffDays = deadline.diff(today, 'day');

                const formattedDate = deadline.format('DD/MM/YYYY');

                if (diffDays < 0) {
                    return <Tag color="error">Quá hạn ({formattedDate})</Tag>;
                } else if (diffDays <= 3) {
                    return <Tag color="warning">Sắp hết ({formattedDate})</Tag>;
                } else {
                    return <Tag color="success">Còn hạn ({formattedDate})</Tag>;
                }
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
            {/* 👈 ĐÂY LÀ CHỖ THIẾU NÚT THÊM MỚI */}
            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '16px' }}>
                <Input.Search
                    placeholder="Tìm kiếm..."
                    onSearch={(value) => fetchData(1, pagination.pageSize, value)}
                    onChange={(e) => setSearchText(e.target.value)}
                    style={{ width: 400 }}
                />
                <Button type="primary" icon={<PlusOutlined />} onClick={showCreateModal}>
                    Thêm mới
                </Button>
            </div>

            <Table
                columns={columns}
                dataSource={data}
                rowKey="id"
                loading={loading}
                pagination={pagination}
                onChange={handleTableChange}
                scroll={{ x: 'max-content' }}
                size="middle"
            />

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
                            <Form.Item name="linh_vuc" label="Lĩnh vực">
                                <Input placeholder="Ví dụ: Giáo dục, Y tế, Xây dựng..." />
                            </Form.Item>
                            <Form.Item
                                name="so_trang"
                                label="Số trang"
                                rules={[
                                    () => ({
                                        validator(_, value) {
                                            if (value !== undefined && value !== null && value < 0) {
                                                return Promise.reject(new Error('Số trang không được là số âm!'));
                                            }
                                            return Promise.resolve();
                                        },
                                    }),
                                ]}
                            >
                                <InputNumber style={{ width: '100%' }} precision={0} />
                            </Form.Item>
                            <Form.Item name="ho_ten_nguoi_ky" label="Họ tên người ký"><Input placeholder="Ví dụ: Nguyễn Văn A" /></Form.Item>
                            <Form.Item name="chuc_vu_nguoi_ky" label="Chức vụ người ký"><Input placeholder="Ví dụ: Giám đốc" /></Form.Item>
                            <Form.Item name="don_vi_nhan" label="Nơi nhận nội bộ"><Input placeholder="Phòng Hành chính, Phòng Kế toán..." /></Form.Item>
                            <Form.Item name="do_khan" label="Mức độ khẩn">
                                <Select allowClear placeholder="Chọn mức độ khẩn">
                                    <Select.Option value={1}>Thường</Select.Option><Select.Option value={2}>Khẩn</Select.Option><Select.Option value={3}>Thượng khẩn</Select.Option><Select.Option value={4}>Hỏa tốc</Select.Option>
                                </Select>
                            </Form.Item>
                            <Form.Item
                                name="han_giai_quyet"
                                label="Hạn giải quyết"
                                dependencies={['ngay_den']}
                                rules={[
                                    ({ getFieldValue }) => ({
                                        validator(_, value) {
                                            // Nếu chưa chọn 1 trong 2 ngày thì bỏ qua không báo lỗi vội
                                            if (!value || !getFieldValue('ngay_den')) return Promise.resolve();

                                            // Nếu Hạn giải quyết < Ngày đến => Bật báo động đỏ!
                                            if (value.isBefore(getFieldValue('ngay_den'), 'day')) {
                                                return Promise.reject(new Error('Hạn giải quyết KHÔNG ĐƯỢC trước Ngày đến!'));
                                            }
                                            return Promise.resolve();
                                        },
                                    }),
                                ]}
                            >
                                <DatePicker style={{ width: '100%' }} format="DD/MM/YYYY" />
                            </Form.Item>
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