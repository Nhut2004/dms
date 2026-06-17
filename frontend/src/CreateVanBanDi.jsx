import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
    Button,
    Card,
    Col,
    DatePicker,
    Form,
    Input,
    Row,
    Select,
    message,
    Spin
} from 'antd';
import axios from 'axios';

const { TextArea } = Input;
const BASE_URL = 'http://localhost:8000';

const CreateVanBanDi = () => {
    const [form] = Form.useForm();
    const navigate = useNavigate();
    const [loading, setLoading] = useState(false);
    const [loadingOptions, setLoadingOptions] = useState(true);
    const [coQuanOptions, setCoQuanOptions] = useState([]);
    const [danhMucOptions, setDanhMucOptions] = useState([]);
    const [hoSoOptions, setHoSoOptions] = useState([]);

    const getAuthHeaders = () => {
        const token = localStorage.getItem('access_token');
        return {
            Authorization: `Bearer ${token}`
        };
    };

    useEffect(() => {
        const fetchOptions = async () => {
            setLoadingOptions(true);
            try {
                const [coQuanRes, danhMucRes, hoSoRes] = await Promise.all([
                    axios.get(`${BASE_URL}/api/co-quan/`, {
                        headers: getAuthHeaders()
                    }),
                    axios.get(`${BASE_URL}/api/danh-muc/`, {
                        headers: getAuthHeaders()
                    }),
                    axios.get(`${BASE_URL}/api/ho-so/`, {
                        headers: getAuthHeaders()
                    })
                ]);

                setCoQuanOptions(
                    (coQuanRes.data || []).map((item) => ({
                        label: item.ten_co_quan,
                        value: item.id
                    }))
                );

                setDanhMucOptions(
                    (danhMucRes.data || []).map((item) => ({
                        label: item.ten_loai_vb,
                        value: item.id
                    }))
                );

                setHoSoOptions(
                    (hoSoRes.data || []).map((item) => ({
                        label: item.ma_ho_so,
                        value: item.ma_ho_so
                    }))
                );
            } catch (error) {
                message.error('Không thể tải dữ liệu dropdown. Vui lòng đăng nhập lại.');
            } finally {
                setLoadingOptions(false);
            }
        };

        fetchOptions();
    }, []);

    const handleSubmit = async (values) => {
        setLoading(true);

        try {
            const payload = {
                so_ky_hieu: values.so_ky_hieu || null,
                ngay_ban_hanh: values.ngay_ban_hanh
                    ? values.ngay_ban_hanh.format('YYYY-MM-DD')
                    : null,
                trich_yeu: values.trich_yeu,
                don_vi_soan_thao_id: values.don_vi_soan_thao_id,
                ma_loai_vb_id: values.ma_loai_vb_id,
                ngon_ngu: values.ngon_ngu || 'Tiếng Việt',
                so_trang: values.so_trang || null,
                ghi_chu: values.ghi_chu || null,
                nguoi_ky_id: values.nguoi_ky_id || null,
                chuc_vu_nguoi_ky: values.chuc_vu_nguoi_ky || null,
                noi_nhan: values.noi_nhan || null,
                muc_do_khan: values.muc_do_khan || null,
                han_tra_loi: values.han_tra_loi
                    ? values.han_tra_loi.format('YYYY-MM-DD')
                    : null,
                stt_trong_ho_so: values.stt_trong_ho_so || null,
                ma_ho_so: values.ma_ho_so || null
            };

            await axios.post(`${BASE_URL}/api/van-ban-di/`, payload, {
                headers: {
                    ...getAuthHeaders(),
                    'Content-Type': 'application/json'
                }
            });

            message.success('Tạo văn bản đi thành công!');
            form.resetFields();
            navigate('/van-ban-di');
        } catch (error) {
            const errorMsg =
                error?.response?.data?.detail ||
                'Có lỗi xảy ra khi tạo văn bản đi.';
            message.error(errorMsg);
        } finally {
            setLoading(false);
        }
    };

    return (
        <Card title="Thêm Văn bản đi" style={{ borderRadius: 12 }}>
            <Spin spinning={loadingOptions}>
                <Form
                    form={form}
                    layout="vertical"
                    onFinish={handleSubmit}
                    initialValues={{
                        ngon_ngu: 'Tiếng Việt'
                    }}
                >
                    <Row gutter={16}>
                        <Col span={12}>
                            <Form.Item label="Số ký hiệu" name="so_ky_hieu">
                                <Input placeholder="VD: VB/2026/001" />
                            </Form.Item>

                            <Form.Item label="Ngày ban hành" name="ngay_ban_hanh">
                                <DatePicker style={{ width: '100%' }} format="YYYY-MM-DD" />
                            </Form.Item>

                            <Form.Item
                                label="Trích yếu"
                                name="trich_yeu"
                                rules={[{ required: true, message: 'Vui lòng nhập trích yếu' }]}
                            >
                                <TextArea rows={4} placeholder="Nhập trích yếu nội dung văn bản" />
                            </Form.Item>

                            <Form.Item
                                label="Đơn vị soạn thảo"
                                name="don_vi_soan_thao_id"
                                rules={[{ required: true, message: 'Vui lòng chọn đơn vị soạn thảo' }]}
                            >
                                <Select
                                    options={coQuanOptions}
                                    placeholder="Chọn đơn vị soạn thảo"
                                    showSearch
                                    filterOption={(input, option) =>
                                        (option?.label ?? '').toLowerCase().includes(input.toLowerCase())
                                    }
                                />
                            </Form.Item>

                            <Form.Item
                                label="Loại văn bản"
                                name="ma_loai_vb_id"
                                rules={[{ required: true, message: 'Vui lòng chọn loại văn bản' }]}
                            >
                                <Select
                                    options={danhMucOptions}
                                    placeholder="Chọn loại văn bản"
                                    showSearch
                                    filterOption={(input, option) =>
                                        (option?.label ?? '').toLowerCase().includes(input.toLowerCase())
                                    }
                                />
                            </Form.Item>

                            <Form.Item label="Ngôn ngữ" name="ngon_ngu">
                                <Input placeholder="Ví dụ: Tiếng Việt" />
                            </Form.Item>

                            <Form.Item label="Số trang" name="so_trang">
                                <Input type="number" placeholder="Nhập số trang" />
                            </Form.Item>

                            <Form.Item label="Ghi chú" name="ghi_chu">
                                <TextArea rows={3} placeholder="Ghi chú thêm" />
                            </Form.Item>
                        </Col>

                        <Col span={12}>
                            <Form.Item label="Người ký" name="nguoi_ky_id">
                                <Select
                                    placeholder="Chọn người ký"
                                    options={[]}
                                />
                            </Form.Item>

                            <Form.Item label="Chức vụ người ký" name="chuc_vu_nguoi_ky">
                                <Input placeholder="Ví dụ: Hiệu trưởng" />
                            </Form.Item>

                            <Form.Item label="Nơi nhận" name="noi_nhan">
                                <Input placeholder="Ví dụ: Phòng Đào tạo" />
                            </Form.Item>

                            <Form.Item label="Mức độ khẩn" name="muc_do_khan">
                                <Select
                                    placeholder="Chọn mức độ khẩn"
                                    options={[
                                        { label: '1', value: 1 },
                                        { label: '2', value: 2 },
                                        { label: '3', value: 3 },
                                        { label: '4', value: 4 },
                                        { label: '5', value: 5 }
                                    ]}
                                />
                            </Form.Item>

                            <Form.Item label="Hạn trả lời" name="han_tra_loi">
                                <DatePicker style={{ width: '100%' }} format="YYYY-MM-DD" />
                            </Form.Item>

                            <Form.Item label="Số thứ tự trong hồ sơ" name="stt_trong_ho_so">
                                <Input type="number" placeholder="Ví dụ: 1" />
                            </Form.Item>

                            <Form.Item label="Mã hồ sơ" name="ma_ho_so">
                                <Select
                                    options={hoSoOptions}
                                    placeholder="Chọn mã hồ sơ"
                                    showSearch
                                    filterOption={(input, option) =>
                                        (option?.label ?? '').toLowerCase().includes(input.toLowerCase())
                                    }
                                />
                            </Form.Item>
                        </Col>
                    </Row>

                    <Row>
                        <Col span={24} style={{ textAlign: 'right' }}>
                            <Button
                                type="default"
                                style={{ marginRight: 8 }}
                                onClick={() => navigate('/van-ban-di')}
                            >
                                Hủy
                            </Button>
                            <Button type="primary" htmlType="submit" loading={loading}>
                                Lưu
                            </Button>
                        </Col>
                    </Row>
                </Form>
            </Spin>
        </Card>
    );
};

export default CreateVanBanDi;
