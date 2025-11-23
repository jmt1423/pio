import { createFileRoute, Link } from '@tanstack/react-router'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { useQuery } from '@tanstack/react-query'
import { Button } from '@/components/ui/button'

export const Route = createFileRoute('/$repoId/')({
  component: RouteComponent,
})

function RouteComponent() {
  const { repoId } = Route.useParams()

  const { isLoading, isError, data, error } = useQuery({
    queryKey: ['repo', repoId],
    queryFn: async () => {
      const response = await fetch(
        `http://localhost:8000/github/repo/${repoId}`,
      )
      if (!response.ok) throw new Error('Failed to fetch repo')
      return response.json()
    },
  })

  if (isLoading) return <div>Loading...</div>
  if (isError) return <div>Error: {error.message}</div>

  return (
    <div className="w-full">
      <div className="flex flex-row gap-2 p-1">
        <Card className="w-full">
          <CardHeader>
            <CardTitle>Pull Requests</CardTitle>
          </CardHeader>
          <CardContent>
            <div>
              {data.pulls.map((pull: any) => (
                <div key={pull.id} className="flex flex-row gap-1">
                  <Button variant={'link'} className="w-fit">
                    <Link
                      to={`/$repoId/$pullNumber`}
                      params={{
                        repoId: `${repoId}`,
                        pullNumber: `${pull.number}`,
                      }}
                    >
                      {pull.title}
                    </Link>
                  </Button>
                  <p className="text-sm text-green-300">{pull.state}</p>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
        <Card className="w-full">
          <CardHeader>
            <CardTitle>Issues</CardTitle>
          </CardHeader>
          <CardContent>
            <div>
              {data.issues.map((issue: any) => (
                <div key={issue.id} className="flex flex-row gap-2">
                  <h3>{issue.title}</h3>
                  <p className="text-sm text-red-300">{issue.state}</p>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
