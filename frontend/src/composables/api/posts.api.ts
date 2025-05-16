import axios from '@/api/client';

export interface Post {
  id: string;
  title: string;
  content: string;
  authorId: string;
  createdAt: string;
  updatedAt?: string;
}

export const fetchPosts = async (): Promise<Post[]> => {
  const response = await axios.get('/posts');
  return response.data;
};

export const createPost = async (postData: Omit<Post, 'id'|'createdAt'>): Promise<Post> => {
  const response = await axios.post('/posts', postData);
  return response.data;
};

export const updatePost = async (id: string, postData: Partial<Post>): Promise<Post> => {
  const response = await axios.patch(`/posts/${id}`, postData);
  return response.data;
};

export const deletePost = async (id: string): Promise<void> => {
  await axios.delete(`/posts/${id}`);
};
