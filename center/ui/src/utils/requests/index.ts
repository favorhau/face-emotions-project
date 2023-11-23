import axios, { AxiosInstance, AxiosRequestConfig, AxiosResponse } from 'axios';

class HttpClient {
  private axiosInstance: AxiosInstance;

  constructor(baseURL: string) {
    this.axiosInstance = axios.create({
      baseURL,
      timeout: 5000, // 设置请求超时时间
      headers: {
        'Content-Type': 'application/json',
        // 其他默认的请求头可以在这里添加
      },
    });

    // 可以在这里添加拦截器等其他配置
  }

  async get<T>(url: string, config?: AxiosRequestConfig): Promise<T> {
    const response: AxiosResponse<T> = await this.axiosInstance.get(url, config);
    return response.data;
  }

  async post<T>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T> {
    const response: AxiosResponse<T> = await this.axiosInstance.post(url, data, config);
    return response.data;
  }

  // 可以添加其他 HTTP 方法，如 put、delete 等

  // 可以添加其他辅助方法

}

const baseURL = 'http://localhost:3000/';
export const httpClient = new HttpClient(baseURL);