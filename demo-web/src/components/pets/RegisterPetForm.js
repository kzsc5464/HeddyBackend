import React, { useState } from 'react';
import { AlertCircle } from 'lucide-react';

const PetRegisterForm = ({ onSuccess }) => {
  const [formData, setFormData] = useState({
    name: '',
    gender: '',
    pet_type: 'DOG', // 기본값
    breed: '',
    weight: '',
    body_type: '',
    birth_date: ''
  });

  const [error, setError] = useState('');

  const petTypes = ['DOG', 'CAT', 'OTHER'];
  const genderTypes = ['수컷', '암컷'];

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      // weight를 숫자로 변환
      const formattedData = {
        ...formData,
        weight: formData.weight ? parseFloat(formData.weight) : null
      };

      const response = await fetch('http://localhost:8000/api/v1/pet', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formattedData)
      });

      const data = await response.json();
      if (response.ok) {
        onSuccess();
      } else {
        setError(data.detail || '등록에 실패했습니다');
      }
    } catch (err) {
      setError('등록 중 오류가 발생했습니다');
    }
  };

  const renderField = (key, label, type = 'text') => {
    if (key === 'pet_type') {
      return (
        <div key={key}>
          <label className="block text-sm font-medium text-gray-700">
            {label}
          </label>
          <select
            value={formData[key]}
            onChange={(e) => setFormData({ ...formData, [key]: e.target.value })}
            className="mt-1 block w-full p-2 border border-gray-300 rounded-md shadow-sm"
            required
          >
            {petTypes.map((type) => (
              <option key={type} value={type}>
                {type}
              </option>
            ))}
          </select>
        </div>
      );
    }

    if (key === 'gender') {
      return (
        <div key={key}>
          <label className="block text-sm font-medium text-gray-700">
            {label}
          </label>
          <select
            value={formData[key]}
            onChange={(e) => setFormData({ ...formData, [key]: e.target.value })}
            className="mt-1 block w-full p-2 border border-gray-300 rounded-md shadow-sm"
            required
          >
            <option value="">선택하세요</option>
            {genderTypes.map((type) => (
              <option key={type} value={type}>
                {type}
              </option>
            ))}
          </select>
        </div>
      );
    }

    return (
      <div key={key}>
        <label className="block text-sm font-medium text-gray-700">
          {label}
        </label>
        <input
          type={type}
          value={formData[key]}
          onChange={(e) => setFormData({ ...formData, [key]: e.target.value })}
          className="mt-1 block w-full p-2 border border-gray-300 rounded-md shadow-sm"
          required={['name'].includes(key)}
        />
      </div>
    );
  };

  const fields = {
    name: '이름',
    gender: '성별',
    pet_type: '반려동물 종류',
    breed: '품종',
    weight: '몸무게 (kg)',
    body_type: '체형',
    birth_date: '생년월일'
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100">
      <div className="p-8 bg-white rounded-lg shadow-md w-96">
        <h2 className="text-2xl font-bold mb-6 text-gray-800 text-center">반려동물 등록</h2>
        {error && (
          <div className="mb-4 p-3 bg-red-100 text-red-700 rounded-md flex items-center">
            <AlertCircle className="w-5 h-5 mr-2" />
            {error}
          </div>
        )}
        <form onSubmit={handleSubmit} className="space-y-4">
          {Object.entries(fields).map(([key, label]) => 
            renderField(key, label, key === 'birth_date' ? 'date' : 
                                  key === 'weight' ? 'number' : 'text')
          )}
          <button
            type="submit"
            className="w-full py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700"
          >
            등록하기
          </button>
        </form>
      </div>
    </div>
  );
};

export default PetRegisterForm;