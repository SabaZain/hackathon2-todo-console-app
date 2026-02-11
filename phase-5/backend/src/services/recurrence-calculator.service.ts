import { RecurrencePattern, RecurrenceFrequency } from '@prisma/client';

export interface RecurrenceCalculationResult {
  nextOccurrence: Date;
  shouldCreateNext: boolean;
}

export class RecurrenceCalculatorService {
  /**
   * Calculate the next occurrence date for a recurring task
   */
  calculateNextOccurrence(
    pattern: RecurrencePattern,
    currentDate: Date = new Date()
  ): RecurrenceCalculationResult {
    const nextDate = new Date(currentDate);

    switch (pattern.frequency) {
      case RecurrenceFrequency.DAILY:
        nextDate.setDate(nextDate.getDate() + pattern.interval);
        break;

      case RecurrenceFrequency.WEEKLY:
        nextDate.setDate(nextDate.getDate() + (7 * pattern.interval));
        // If dayOfWeek is specified, adjust to that day
        if (pattern.dayOfWeek !== null) {
          const currentDay = nextDate.getDay();
          const targetDay = pattern.dayOfWeek;
          const daysToAdd = (targetDay - currentDay + 7) % 7;
          nextDate.setDate(nextDate.getDate() + daysToAdd);
        }
        break;

      case RecurrenceFrequency.MONTHLY:
        nextDate.setMonth(nextDate.getMonth() + pattern.interval);
        // Handle day of month
        if (pattern.dayOfMonth !== null) {
          const targetDay = pattern.dayOfMonth;
          const lastDayOfMonth = new Date(
            nextDate.getFullYear(),
            nextDate.getMonth() + 1,
            0
          ).getDate();
          // If target day doesn't exist in month, use last day
          nextDate.setDate(Math.min(targetDay, lastDayOfMonth));
        }
        break;

      case RecurrenceFrequency.YEARLY:
        nextDate.setFullYear(nextDate.getFullYear() + pattern.interval);
        break;

      case RecurrenceFrequency.CUSTOM:
        // For custom patterns, use interval as days
        nextDate.setDate(nextDate.getDate() + pattern.interval);
        break;

      default:
        throw new Error(`Unsupported recurrence frequency: ${pattern.frequency}`);
    }

    // Check if we should create the next occurrence
    const shouldCreateNext = this.shouldCreateNextOccurrence(pattern, nextDate);

    return {
      nextOccurrence: nextDate,
      shouldCreateNext,
    };
  }

  /**
   * Determine if the next occurrence should be created based on end conditions
   */
  private shouldCreateNextOccurrence(pattern: RecurrencePattern, nextDate: Date): boolean {
    // Check end date
    if (pattern.endDate && nextDate > pattern.endDate) {
      return false;
    }

    // Check occurrences count (would need to track in database)
    // This is a simplified check - in production, you'd query the database
    // to count existing occurrences
    if (pattern.occurrencesCount !== null) {
      // This would require database query to count existing tasks
      // For now, we'll assume it's handled elsewhere
    }

    return true;
  }

  /**
   * Validate a recurrence pattern
   */
  validatePattern(pattern: Partial<RecurrencePattern>): { valid: boolean; errors: string[] } {
    const errors: string[] = [];

    if (!pattern.frequency) {
      errors.push('Frequency is required');
    }

    if (pattern.interval !== undefined && pattern.interval < 1) {
      errors.push('Interval must be at least 1');
    }

    if (pattern.frequency === RecurrenceFrequency.WEEKLY && pattern.dayOfWeek !== null && pattern.dayOfWeek !== undefined) {
      if (pattern.dayOfWeek < 0 || pattern.dayOfWeek > 6) {
        errors.push('Day of week must be between 0 (Sunday) and 6 (Saturday)');
      }
    }

    if (pattern.frequency === RecurrenceFrequency.MONTHLY && pattern.dayOfMonth !== null && pattern.dayOfMonth !== undefined) {
      if (pattern.dayOfMonth < 1 || pattern.dayOfMonth > 31) {
        errors.push('Day of month must be between 1 and 31');
      }
    }

    if (pattern.endDate && pattern.occurrencesCount !== null) {
      errors.push('Cannot specify both end date and occurrences count');
    }

    return {
      valid: errors.length === 0,
      errors,
    };
  }

  /**
   * Generate a human-readable description of the recurrence pattern
   */
  describePattern(pattern: RecurrencePattern): string {
    const { frequency, interval, dayOfWeek, dayOfMonth } = pattern;

    switch (frequency) {
      case RecurrenceFrequency.DAILY:
        return interval === 1 ? 'Daily' : `Every ${interval} days`;

      case RecurrenceFrequency.WEEKLY:
        const dayNames = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
        const dayText = dayOfWeek !== null ? ` on ${dayNames[dayOfWeek]}` : '';
        return interval === 1 ? `Weekly${dayText}` : `Every ${interval} weeks${dayText}`;

      case RecurrenceFrequency.MONTHLY:
        const dayText2 = dayOfMonth !== null ? ` on day ${dayOfMonth}` : '';
        return interval === 1 ? `Monthly${dayText2}` : `Every ${interval} months${dayText2}`;

      case RecurrenceFrequency.YEARLY:
        return interval === 1 ? 'Yearly' : `Every ${interval} years`;

      case RecurrenceFrequency.CUSTOM:
        return `Every ${interval} days (custom)`;

      default:
        return 'Unknown pattern';
    }
  }
}

export const recurrenceCalculator = new RecurrenceCalculatorService();
