import httpClient from '@/utils/httpClient';

export interface Post {
  id: string;
  title: string;
  content: string;
  authorId: string;
  createdAt: string;
  updatedAt?: string;
}

export interface CreatePostDto extends Omit<Post, 'id' | 'createdAt' | 'updatedAt'> {}
export interface UpdatePostDto extends Partial<Omit<Post, 'id' | 'authorId' | 'createdAt'>> {}

export const fetchPosts = async (): Promise<Post[]> => {
  try {
    const response = await httpClient.get<Post[]>('/posts');
    return response.data;
  } catch (error) {
    console.error('Error fetching posts:', error);
    throw error;
  }
};

export const createPost = async (postData: CreatePostDto): Promise<Post> => {
  try {
    const response = await httpClient.post<Post>('/posts', postData);
    return response.data;
  } catch (error) {
    console.error('Error creating post:', error);
    throw error;
  }
};

export const updatePost = async (id: string, postData: UpdatePostDto): Promise<Post> => {
  try {
    const response = await httpClient.patch<Post>(`/posts/${id}`, postData);
    return response.data;
  } catch (error) {
    console.error(`Error updating post ${id}:`, error);
    throw error;
  }
};

export const deletePost = async (id: string): Promise<void> => {
  try {
    await httpClient.delete(`/posts/${id}`);
  } catch (error) {
    console.error(`Error deleting post ${id}:`, error);
    throw error;
  }
};
