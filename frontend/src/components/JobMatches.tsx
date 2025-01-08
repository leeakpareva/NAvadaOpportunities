// Removed unused FC import
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card'
import { Badge } from './ui/badge'
import { Progress } from './ui/progress'
import { Button } from './ui/button'
import { Sparkles } from 'lucide-react'
import { motion } from 'framer-motion'
import type { JobMatch } from '../types/files'

interface JobMatchesProps {
  matches: JobMatch[]
  isLoading?: boolean
}

export function JobMatches({ matches, isLoading }: JobMatchesProps) {
  const container = {
    hidden: { opacity: 0 },
    show: {
      opacity: 1,
      transition: {
        staggerChildren: 0.1
      }
    }
  }

  const item = {
    hidden: { opacity: 0, y: 20 },
    show: { opacity: 1, y: 0 }
  }

  if (isLoading) {
    return (
      <Card className="bg-white/5 backdrop-blur-sm border-white/10">
        <CardContent className="py-8">
          <div className="text-center text-white/60">Finding matching opportunities...</div>
        </CardContent>
      </Card>
    )
  }

  if (matches.length === 0) {
    return (
      <Card className="bg-white/5 backdrop-blur-sm border-white/10">
        <CardContent className="py-8">
          <div className="text-center text-white/60">
            No matching opportunities found. Try adjusting your preferences or uploading an updated CV.
          </div>
        </CardContent>
      </Card>
    )
  }

  return (
    <motion.div variants={container} initial="hidden" animate="show" className="space-y-4">
      {matches.map((match) => (
        <motion.div key={match.job.id} variants={item}>
          <Card className="bg-white/5 backdrop-blur-sm border-white/10 hover:bg-white/10 transition-all duration-300">
            <CardHeader>
              <div className="flex justify-between items-start">
                <div>
                  <CardTitle className="text-xl mb-1 text-white flex items-center gap-2">
                    {match.job.title}
                    {match.score_details.high_priority && (
                      <Badge className="bg-amber-500/20 text-amber-200">High Match</Badge>
                    )}
                  </CardTitle>
                  <CardDescription className="text-white/60">
                    {match.job.company} • {match.job.location} • 
                    {match.job.employment_type} •
                    {match.job.salary_range?.min ? 
                      <>
                        {' £'}{match.job.salary_range.min.toLocaleString()}
                        {match.job.salary_range.max && ` - £${match.job.salary_range.max.toLocaleString()}`}
                      </> 
                      : ' Salary not specified'}
                  </CardDescription>
                </div>
                {match.job.url && (
                  <motion.div whileHover={{ scale: 1.05 }}>
                    <a
                      href={match.job.url}
                      target="_blank"
                      rel="noopener noreferrer"
                    >
                      <Button size="sm" className="bg-white/10 hover:bg-white/20 text-white">
                        <Sparkles className="h-4 w-4 mr-2" />
                        View Job
                      </Button>
                    </a>
                  </motion.div>
                )}
              </div>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-white/60 mb-4">{match.job.description}</p>
              
              <div className="space-y-3">
                <div>
                  <div className="flex justify-between text-sm mb-1">
                    <span className="text-white/60">Technical Match</span>
                    <span className="text-white">
                      {(match.score_details.category_scores.technical * 100).toFixed(0)}%
                    </span>
                  </div>
                  <Progress 
                    value={match.score_details.category_scores.technical * 100} 
                    className="h-1.5 bg-white/10"
                  />
                </div>
                
                <div>
                  <div className="flex justify-between text-sm mb-1">
                    <span className="text-white/60">Artistic Match</span>
                    <span className="text-white">
                      {(match.score_details.category_scores.artistic * 100).toFixed(0)}%
                    </span>
                  </div>
                  <Progress 
                    value={match.score_details.category_scores.artistic * 100} 
                    className="h-1.5 bg-white/10"
                  />
                </div>

                <div>
                  <div className="flex justify-between text-sm mb-1">
                    <span className="text-white/60">Overall Match</span>
                    <div className="flex items-center gap-2">
                      <span className="text-white">
                        {(match.score_details.total_score * 100).toFixed(0)}%
                      </span>
                      {match.score_details.high_priority && (
                        <span className="px-2 py-0.5 text-xs bg-amber-500/20 text-amber-200 rounded">
                          High Match
                        </span>
                      )}
                    </div>
                  </div>
                  <Progress 
                    value={match.score_details.total_score * 100} 
                    className="h-1.5 bg-white/10"
                  />
                </div>
              </div>

              <div className="mt-4 flex flex-wrap gap-2">
                {match.score_details.matched_keywords.map((keyword) => (
                  <Badge 
                    key={keyword}
                    variant="secondary"
                    className="bg-white/5 text-white hover:bg-white/10 transition-colors"
                  >
                    {keyword}
                  </Badge>
                ))}
              </div>
            </CardContent>
          </Card>
        </motion.div>
      ))}
    </motion.div>
  )
}
