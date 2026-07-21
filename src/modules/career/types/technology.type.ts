export interface Technology {
  id: string
  name: string
  category: string | null
  layer: string | null
}

export interface ITechnologyService {
  search(query?: string, limit?: number): Promise<Technology[]>
}
