<script setup lang="ts">
import { Sparkles } from 'lucide-vue-next'
import { ref } from 'vue'
import { useI18n } from 'vue-i18n'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { useAnalyzeProfile } from '@/modules/career/composables/useCareerAi'
import { useHandleError } from '@/shared/composables/useHandleError'
import type { AnalyzeProfileResult } from '@/modules/career/types/ai.type'

const { t } = useI18n()
const { handleError } = useHandleError()
const { mutateAsync: analyzeProfile, isPending: isAnalyzing } = useAnalyzeProfile()

const targetRole = ref('')
const result = ref<AnalyzeProfileResult | null>(null)

async function handleAnalyze() {
  const role = targetRole.value.trim()
  if (!role) return
  try {
    result.value = await analyzeProfile(role)
  } catch (error) {
    handleError(error, { fallbackMessage: t('career.ai.error.accessDenied') })
  }
}
</script>

<template>
  <Card>
    <CardHeader>
      <div class="flex items-center gap-2">
        <Sparkles :size="20" />
        <CardTitle>{{ t('career.ai.gapAnalysis.title') }}</CardTitle>
      </div>
      <CardDescription>{{ t('career.ai.gapAnalysis.subtitle') }}</CardDescription>
    </CardHeader>
    <CardContent class="space-y-4">
      <div class="flex gap-2">
        <Input
          v-model="targetRole"
          :placeholder="t('career.ai.gapAnalysis.targetRolePlaceholder')"
          @keydown.enter.prevent="handleAnalyze"
        />
        <Button
          type="button"
          :disabled="!targetRole.trim()"
          :loading="isAnalyzing"
          @click="handleAnalyze"
        >
          {{ t('career.ai.gapAnalysis.button') }}
        </Button>
      </div>

      <p v-if="!result" class="text-sm text-muted-foreground">
        {{ t('career.ai.gapAnalysis.empty') }}
      </p>

      <div v-else class="space-y-4">
        <div class="flex items-center gap-2">
          <span class="text-sm font-medium">{{ t('career.ai.gapAnalysis.matchScore') }}</span>
          <Badge variant="default">
            {{ result.matchScore }}%
          </Badge>
        </div>

        <div v-if="result.strengths.length" class="space-y-1">
          <p class="text-sm font-medium">
            {{ t('career.ai.gapAnalysis.strengths') }}
          </p>
          <ul class="list-disc pl-5 text-sm space-y-1">
            <li v-for="(item, i) in result.strengths" :key="i">
              {{ item }}
            </li>
          </ul>
        </div>

        <div v-if="result.gaps.length" class="space-y-1">
          <p class="text-sm font-medium">
            {{ t('career.ai.gapAnalysis.gaps') }}
          </p>
          <ul class="list-disc pl-5 text-sm space-y-1">
            <li v-for="(item, i) in result.gaps" :key="i">
              {{ item }}
            </li>
          </ul>
        </div>

        <div v-if="result.recommendations.length" class="space-y-1">
          <p class="text-sm font-medium">
            {{ t('career.ai.gapAnalysis.recommendations') }}
          </p>
          <ul class="list-disc pl-5 text-sm space-y-1">
            <li v-for="(item, i) in result.recommendations" :key="i">
              {{ item }}
            </li>
          </ul>
        </div>
      </div>
    </CardContent>
  </Card>
</template>
