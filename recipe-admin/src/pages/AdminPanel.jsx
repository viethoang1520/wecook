import React, { useState } from 'react'
import './AdminPanel.scss'
import { Button, Upload, message, Spin, Form, Input, Space, Typography, Select } from 'antd'
import axios from 'axios'

const { TextArea } = Input;
const { Title } = Typography;

export default function AdminPanel() {
  const [file, setFile] = useState(null); // Lưu file đã upload
  const [loading, setLoading] = useState(false); // Hiển thị loading
  const [recipeData, setRecipeData] = useState(null); // Kết quả API trả về
  const [form] = Form.useForm();

  const CATEGORIES = [
    { value: 'Món chính', label: 'Món chính' },
    { value: 'Món ăn nhẹ', label: 'Món ăn nhẹ' },
    { value: 'Món tráng miệng', label: 'Món tráng miệng' },
    { value: 'Món khai vị', label: 'Món khai vị' },
    { value: 'Đồ uống', label: 'Đồ uống' },
  ];

  const handleBeforeUpload = (file) => {
    console.log(file)
    setFile(file);
    return false; // Prevent from automated upload
  };

  // Call API handle uploading video
  const handleUpload = async () => {
    if (!file) {
      message.error("Vui lòng chọn video trước khi upload!");
      return;
    }

    const formData = new FormData();
    formData.append("video", file);

    try {
      setLoading(true);
      const response = await axios.post("http://localhost:8000/api/recipes/upload_video/", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });

      setRecipeData(response.data);
      // Chuẩn bị dữ liệu cho form
      const recipe = response.data.recipe_json.recipe;
      form.setFieldsValue({
        name: recipe.name,
        category: recipe.category,
        ingredients: recipe.ingredients.map(ing => ({
          name: ing.name,
          quantity: ing.quantity,
          unit: ing.unit
        })),
        steps: recipe.steps.map(step => ({
          step: step.step,
          description: step.description
        })),
        notes: recipe.notes
      });

      message.success("Video đã được xử lý thành công!");
    } catch (error) {
      console.error("Error response:", error.response?.data);
      message.error("Có lỗi xảy ra trong quá trình xử lý video.");
    } finally {
      setLoading(false);
    }
  };

  // Thêm hàm handleFormSubmit vào đây
  const handleFormSubmit = async (values) => {
    try {
      const formattedData = {
        recipe_json: {
          recipe: {
            ...values,
            ingredients: values.ingredients.map(ing => ({
              name: ing.name,
              quantity: ing.quantity,
              unit: ing.unit
            })),
            steps: values.steps.map((step, index) => ({
              step: index + 1,
              description: step.description
            }))
          }
        }
      };

      // await axios.post('http://localhost:8000/api/recipes/save/', formattedData);
      message.success('Đã lưu công thức thành công!');
    } catch (error) {
      console.error(error);
      message.error('Có lỗi xảy ra khi lưu công thức.');
    }
  };

  return (
    <div className='container' style={{ padding: '24px' }}>
      <Upload
        beforeUpload={handleBeforeUpload}
        maxCount={1}
        accept="video/*"
      >
        <Button>Chọn Video</Button>
      </Upload>

      <Button 
        onClick={handleUpload} 
        type="primary" 
        style={{ marginTop: '16px', marginBottom: '16px' }}
        loading={loading}
      >
        Upload và Xử lý
      </Button>

      {loading && <Spin tip="Đang xử lý video..." />}

      {recipeData && (
        <Form
          form={form}
          layout="vertical"
          onFinish={handleFormSubmit}
          style={{ marginTop: '24px' }}
        >
          <Title level={4}>Thông tin công thức</Title>
          
          <Form.Item
            label="Tên món ăn"
            name="name"
            rules={[{ required: true }]}
          >
            <Input />
          </Form.Item>

          <Form.Item
            label="Danh mục"
            name="category"
            rules={[{ required: true, message: 'Vui lòng chọn danh mục!' }]}
          >
            <Select
              options={CATEGORIES}
              placeholder="Chọn danh mục món ăn"
            />
          </Form.Item>

          <Title level={4}>Nguyên liệu</Title>
          <Form.List name="ingredients">
            {(fields, { add, remove }) => (
              <>
                {fields.map(({ key, name, ...restField }) => (
                  <Space key={key} style={{ display: 'flex', marginBottom: 8 }} align="baseline">
                    <Form.Item
                      {...restField}
                      name={[name, 'name']}
                      label="Tên"
                    >
                      <Input placeholder="Tên nguyên liệu" />
                    </Form.Item>
                    <Form.Item
                      {...restField}
                      name={[name, 'quantity']}
                      label="Số lượng"
                    >
                      <Input placeholder="Số lượng" />
                    </Form.Item>
                    <Form.Item
                      {...restField}
                      name={[name, 'unit']}
                      label="Đơn vị"
                    >
                      <Input placeholder="Đơn vị" />
                    </Form.Item>
                  </Space>
                ))}
              </>
            )}
          </Form.List>

          <Title level={4}>Các bước thực hiện</Title>
          <Form.List name="steps">
            {(fields, { add, remove }) => (
              <>
                {fields.map(({ key, name, ...restField }) => (
                  <Space key={key} style={{ display: 'flex', marginBottom: 8 }} align="baseline">
                    <Form.Item
                      {...restField}
                      name={[name, 'step']}
                      label="Bước"
                    >
                      <Input disabled style={{ width: '60px' }} />
                    </Form.Item>
                    <Form.Item
                      {...restField}
                      name={[name, 'description']}
                      label="Mô tả"
                      style={{ width: '500px' }}
                    >
                      <TextArea rows={2} />
                    </Form.Item>
                  </Space>
                ))}
              </>
            )}
          </Form.List>

          <Form.Item
            label="Ghi chú"
            name="notes"
          >
            <TextArea rows={4} />
          </Form.Item>

          <Form.Item>
            <Button type="primary" htmlType="submit">
              Save recipe
            </Button>
          </Form.Item>
        </Form>
      )}
    </div>
  )
}
